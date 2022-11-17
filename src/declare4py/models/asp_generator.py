from __future__ import annotations

import collections
import json
import os
import typing
from random import randrange

import clingo
from clingo import SymbolType

from pm4py.objects.log import obj as lg
from pm4py.objects.log.exporter.xes import exporter

from src.declare4py.core.log_generator import LogGenerator
from src.declare4py.log_utils.parsers.declare.decl_model import DeclModel
from src.declare4py.log_utils.log_analyzer import LogAnalyzer
from src.declare4py.models.log_generation.declare2Lp import Declare2lp
from src.declare4py.models.log_generation.distribution import Distributor
from datetime import datetime


class ASPCustomEventModel:
    name: str
    pos: int
    resource: {str, str} = {}

    def __init__(self, fact_symbol: [clingo.symbol.Symbol]):
        self.fact_symbol = fact_symbol
        self.parse_clingo_event()
        self.resource = {}

    def parse_clingo_event(self):
        for symbols in self.fact_symbol:
            if symbols.type == SymbolType.Function:
                self.name = str(symbols.name)
            if symbols.type == SymbolType.Number:
                self.pos = symbols.number

    def __str__(self) -> str:
        st = f"""{{ "event_name":"{self.name}", "position": "{self.pos}", "resource_or_value": {self.resource} }}"""
        return st.replace("'", '"')

    def __repr__(self) -> str:
        return self.__str__()


class ASPCustomTraceModel:
    name: str
    events: [ASPCustomEventModel] = []

    def __init__(self, trace_name: str, model: [clingo.solving.Model]):
        self.model = model
        self.name = trace_name
        self.events = []
        self.parse_clingo_trace()

    def parse_clingo_trace(self):
        e = {}
        assigned_values_symbols = []
        for m in self.model:  # self.model = [trace(),.. trace(),.., assigned_value(...),...]
            trace_name = str(m.name)
            if trace_name == "trace":  # fact "trace(event_name, position)"
                eventModel = ASPCustomEventModel(m.arguments)
                e[eventModel.pos] = eventModel
                self.events.append(eventModel)
            if trace_name == "assigned_value":
                assigned_values_symbols.append(m.arguments)

        for assigned_value_symbol in assigned_values_symbols:
            resource_name, resource_val, pos = self.parse_clingo_val_assignement(assigned_value_symbol)
            event = e[pos]
            event.resource[resource_name] = resource_val

    def parse_clingo_val_assignement(self, syb: [clingo.symbol.Symbol]):
        val = []
        for symbols in syb:
            if symbols.type == SymbolType.Function:  # if symbol is functionm it can have .arguments
                val.append(symbols.name)
            else:
                val.append(symbols.number)
        return val[0], val[1], val[2]

    def __str__(self):
        st = f"""{{ "trace_name": "{self.name}", "events": {self.events} }}"""
        return st.replace("'", '"')

    def __repr__(self):
        return self.__str__()


class AspCustomLogModel:
    traces: [ASPCustomTraceModel] = []

    def __init__(self):
        self.traces: [ASPCustomTraceModel] = []

    def __str__(self):
        return str(self.traces)

    def __repr__(self):
        return self.__str__()

    def print_indent(self):
        s = self.__str__()
        j = json.loads(s)
        print(json.dumps(j, indent=2))


class AspGenerator(LogGenerator):

    def __init__(self, num_traces: int, min_event: int, max_event: int,
                 decl_model: DeclModel, template_path: str, encoding_path: str,
                 log: LogAnalyzer = None,
                 distributor_type: typing.Literal["uniform", "normal", "custom"] = "uniform",
                 custom_probabilities: typing.Optional[typing.List[float]] = None
                 ):
        super().__init__(num_traces, min_event, max_event, log, decl_model)
        self.template_path = template_path
        self.encoding_path = encoding_path
        self.clingo_output = []
        self.asp_custom_structure: AspCustomLogModel | None = None
        d = Distributor()
        self.traces_length: collections.Counter | None = d.distribution(min_event, max_event, num_traces,
                                                                        distributor_type, custom_probabilities)

    def __decl_model2lp_file(self):
        # with open(self.decl_model_path, "r") as file:
        #     d2a = DeclareParser(file.read())
        #     dm = d2a.parse()
        lp_model = Declare2lp().from_decl(self.decl_model)
        lp = lp_model.__str__()
        filename = "generated.lp"
        # with tempfile.NamedTemporaryFile() as tmp:  # TODO: improve it
        with open(filename, "w+") as tmp:
            tmp.write(lp)
        return filename

    def run(self):
        decl2lp_file = self.__decl_model2lp_file()
        self.clingo_output = []
        for events, traces in self.traces_length.items():
            random_seed = randrange(0, 2 ** 32 - 1)
            self.__generate_asp_trace(decl2lp_file, events, traces, random_seed)
        self.__format_to_custom_asp_structure()
        self.__pm4py_log()
        os.remove(decl2lp_file)  # removes the temporary decl->lp modal file created

    def __format_to_custom_asp_structure(self):
        self.asp_custom_structure = AspCustomLogModel()
        asp_model = self.asp_custom_structure
        i = 0
        for clingo_trace in self.clingo_output:
            trace_model = ASPCustomTraceModel(f"trace_{i}", clingo_trace)
            asp_model.traces.append(trace_model)
            i = i + 1

    def __generate_asp_trace(self, decl_model_lp_file: str, num_events: int, num_traces: int,
                             seed: int, freq: float = 0.9, ):
        ctl = clingo.Control(
            [f"-c t={num_events}", f"{num_traces}", f"--seed={seed}", f"--rand-freq={freq}"])  # TODO: add parameters
        ctl.load(self.encoding_path)
        ctl.load(self.template_path)
        ctl.load(decl_model_lp_file)
        ctl.ground([("base", [])], context=self)
        ctl.solve(on_model=self.__handle_clingo_result)

    def __handle_clingo_result(self, output: clingo.solving.Model):
        symbols = output.symbols(shown=True)
        self.clingo_output.append(symbols)

    def __pm4py_log(self):

        self.log_analyzer.log = lg.EventLog()
        self.log_analyzer.log.extensions["concept"] = {}  # TODO: add which extensions?
        self.log_analyzer.log.extensions["concept"]["name"] = lg.XESExtension.Concept.name
        self.log_analyzer.log.extensions["concept"]["prefix"] = lg.XESExtension.Concept.prefix
        self.log_analyzer.log.extensions["concept"]["uri"] = lg.XESExtension.Concept.uri

        for trace in self.asp_custom_structure.traces:
            trace_gen = lg.Trace()
            trace_gen.attributes["concept:name"] = trace.name
            for asp_event in trace.events:
                event = lg.Event()
                event["concept:name"] = asp_event.name
                for res_name, res_value in asp_event.resource.items():
                    event[res_name] = res_value
                event["time:timestamp"] = datetime.now().timestamp()  # + timedelta(hours=c).datetime
                trace_gen.append(event)
            self.log_analyzer.log.append(trace_gen)

    def to_xes(self, output_fn: str):
        if self.log_analyzer.log is None:
            self.__pm4py_log()
        exporter.apply(self.log_analyzer.log, output_fn)
