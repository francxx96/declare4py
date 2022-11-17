automaton("Absence2",s_1,c,s_1).
automaton("Absence2",s_2,c,s_2).
automaton("Absence2",s_2,a,s_2).
automaton("Absence2",s_0,c,s_0).
automaton("Absence2",s_1,a,s_2).
automaton("Absence2",s_0,a,s_1).

initial("Absence2",s_0).

accepting("Absence2",s_0).
accepting("Absence2",s_1).


automaton("Absence3",s_0,a,s_3).
automaton("Absence3",s_1,c,s_1).
automaton("Absence3",s_2,c,s_2).
automaton("Absence3",s_3,c,s_3).
automaton("Absence3",s_2,a,s_2).
automaton("Absence3",s_0,c,s_0).
automaton("Absence3",s_3,a,s_1).
automaton("Absence3",s_1,a,s_2).

initial("Absence3",s_0).

accepting("Absence3",s_0).
accepting("Absence3",s_1).
accepting("Absence3",s_3).


automaton("Absence",s_1,c,s_1).
automaton("Absence",s_0,c,s_0).
automaton("Absence",s_1,a,s_1).
automaton("Absence",s_0,a,s_1).

initial("Absence",s_0).

accepting("Absence",s_0).


automaton("Alternate_Precedence",s_2,c,s_2).
automaton("Alternate_Precedence",s_3,c,s_3).
automaton("Alternate_Precedence",s_0,c,s_4).
automaton("Alternate_Precedence",s_2,a,s_2).
automaton("Alternate_Precedence",s_1,a,s_3).
automaton("Alternate_Precedence",s_1,c,s_3).
automaton("Alternate_Precedence",s_0,a,s_2).
automaton("Alternate_Precedence",s_2,b,s_4).
automaton("Alternate_Precedence",s_0,b,s_3).
automaton("Alternate_Precedence",s_4,a,s_2).
automaton("Alternate_Precedence",s_4,c,s_4).
automaton("Alternate_Precedence",s_3,a,s_3).
automaton("Alternate_Precedence",s_3,b,s_3).
automaton("Alternate_Precedence",s_4,b,s_3).
automaton("Alternate_Precedence",s_1,b,s_3).

initial("Alternate_Precedence",s_0).

accepting("Alternate_Precedence",s_0).
accepting("Alternate_Precedence",s_1).
accepting("Alternate_Precedence",s_2).
accepting("Alternate_Precedence",s_4).


automaton("Alternate_Response",s_1,c,s_1).
automaton("Alternate_Response",s_2,c,s_2).
automaton("Alternate_Response",s_2,a,s_2).
automaton("Alternate_Response",s_2,b,s_2).
automaton("Alternate_Response",s_0,c,s_0).
automaton("Alternate_Response",s_0,b,s_0).
automaton("Alternate_Response",s_0,a,s_1).
automaton("Alternate_Response",s_1,a,s_2).
automaton("Alternate_Response",s_1,b,s_0).

initial("Alternate_Response",s_0).

accepting("Alternate_Response",s_0).


automaton("Alternate_Succession",s_1,c,s_1).
automaton("Alternate_Succession",s_2,c,s_2).
automaton("Alternate_Succession",s_2,a,s_2).
automaton("Alternate_Succession",s_2,b,s_2).
automaton("Alternate_Succession",s_0,c,s_0).
automaton("Alternate_Succession",s_1,a,s_2).
automaton("Alternate_Succession",s_0,a,s_1).
automaton("Alternate_Succession",s_1,b,s_0).
automaton("Alternate_Succession",s_0,b,s_2).

initial("Alternate_Succession",s_0).

accepting("Alternate_Succession",s_0).


automaton("Chain_Precedence",s_2,c,s_2).
automaton("Chain_Precedence",s_4,c,s_2).
automaton("Chain_Precedence",s_4,b,s_2).
automaton("Chain_Precedence",s_2,b,s_3).
automaton("Chain_Precedence",s_0,b,s_1).
automaton("Chain_Precedence",s_3,c,s_3).
automaton("Chain_Precedence",s_1,c,s_3).
automaton("Chain_Precedence",s_1,a,s_3).
automaton("Chain_Precedence",s_2,a,s_4).
automaton("Chain_Precedence",s_3,a,s_3).
automaton("Chain_Precedence",s_3,b,s_3).
automaton("Chain_Precedence",s_0,a,s_4).
automaton("Chain_Precedence",s_4,a,s_4).
automaton("Chain_Precedence",s_0,c,s_2).
automaton("Chain_Precedence",s_1,b,s_3).

initial("Chain_Precedence",s_0).

accepting("Chain_Precedence",s_0).
accepting("Chain_Precedence",s_1).
accepting("Chain_Precedence",s_2).
accepting("Chain_Precedence",s_4).


automaton("Chain_Response",s_2,c,s_2).
automaton("Chain_Response",s_2,a,s_2).
automaton("Chain_Response",s_2,b,s_2).
automaton("Chain_Response",s_0,c,s_0).
automaton("Chain_Response",s_0,b,s_0).
automaton("Chain_Response",s_0,a,s_1).
automaton("Chain_Response",s_1,a,s_2).
automaton("Chain_Response",s_1,c,s_2).
automaton("Chain_Response",s_1,b,s_0).

initial("Chain_Response",s_0).

accepting("Chain_Response",s_0).


automaton("Chain_Succession",s_0,a,s_3).
automaton("Chain_Succession",s_1,c,s_1).
automaton("Chain_Succession",s_0,c,s_4).
automaton("Chain_Succession",s_2,c,s_1).
automaton("Chain_Succession",s_3,b,s_4).
automaton("Chain_Succession",s_4,a,s_3).
automaton("Chain_Succession",s_4,b,s_1).
automaton("Chain_Succession",s_1,b,s_1).
automaton("Chain_Succession",s_3,a,s_1).
automaton("Chain_Succession",s_4,c,s_4).
automaton("Chain_Succession",s_2,a,s_1).
automaton("Chain_Succession",s_2,b,s_1).
automaton("Chain_Succession",s_1,a,s_1).
automaton("Chain_Succession",s_3,c,s_1).
automaton("Chain_Succession",s_0,b,s_2).

initial("Chain_Succession",s_0).

accepting("Chain_Succession",s_0).
accepting("Chain_Succession",s_2).
accepting("Chain_Succession",s_4).


automaton("Choice",s_1,c,s_1).
automaton("Choice",s_0,b,s_1).
automaton("Choice",s_0,c,s_0).
automaton("Choice",s_1,b,s_1).
automaton("Choice",s_0,a,s_1).
automaton("Choice",s_1,a,s_1).

initial("Choice",s_0).

accepting("Choice",s_1).


automaton("CoExistence",s_0,a,s_3).
automaton("CoExistence",s_1,c,s_1).
automaton("CoExistence",s_2,c,s_2).
automaton("CoExistence",s_3,b,s_1).
automaton("CoExistence",s_3,c,s_3).
automaton("CoExistence",s_2,b,s_2).
automaton("CoExistence",s_0,c,s_0).
automaton("CoExistence",s_1,b,s_1).
automaton("CoExistence",s_2,a,s_1).
automaton("CoExistence",s_1,a,s_1).
automaton("CoExistence",s_3,a,s_3).
automaton("CoExistence",s_0,b,s_2).

initial("CoExistence",s_0).

accepting("CoExistence",s_0).
accepting("CoExistence",s_1).


automaton("End",s_1,c,s_0).
automaton("End",s_0,c,s_0).
automaton("End",s_1,a,s_1).
automaton("End",s_0,a,s_1).

initial("End",s_0).

accepting("End",s_1).


automaton("Exactly1",s_1,c,s_1).
automaton("Exactly1",s_2,c,s_2).
automaton("Exactly1",s_2,a,s_2).
automaton("Exactly1",s_0,c,s_0).
automaton("Exactly1",s_1,a,s_2).
automaton("Exactly1",s_0,a,s_1).

initial("Exactly1",s_0).

accepting("Exactly1",s_1).


automaton("Exactly2",s_1,c,s_1).
automaton("Exactly2",s_2,c,s_2).
automaton("Exactly2",s_3,c,s_3).
automaton("Exactly2",s_2,a,s_2).
automaton("Exactly2",s_3,a,s_2).
automaton("Exactly2",s_1,a,s_3).
automaton("Exactly2",s_0,c,s_0).
automaton("Exactly2",s_0,a,s_1).

initial("Exactly2",s_0).

accepting("Exactly2",s_3).


automaton("Exclusive_Choice",s_1,c,s_1).
automaton("Exclusive_Choice",s_2,c,s_2).
automaton("Exclusive_Choice",s_2,b,s_3).
automaton("Exclusive_Choice",s_0,b,s_1).
automaton("Exclusive_Choice",s_3,c,s_3).
automaton("Exclusive_Choice",s_2,a,s_2).
automaton("Exclusive_Choice",s_1,a,s_3).
automaton("Exclusive_Choice",s_0,a,s_2).
automaton("Exclusive_Choice",s_0,c,s_0).
automaton("Exclusive_Choice",s_1,b,s_1).
automaton("Exclusive_Choice",s_3,b,s_3).
automaton("Exclusive_Choice",s_3,a,s_3).

initial("Exclusive_Choice",s_0).

accepting("Exclusive_Choice",s_1).
accepting("Exclusive_Choice",s_2).


automaton("Existence2",s_2,c,s_2).
automaton("Existence2",s_1,c,s_1).
automaton("Existence2",s_0,a,s_2).
automaton("Existence2",s_0,c,s_0).
automaton("Existence2",s_2,a,s_1).
automaton("Existence2",s_1,a,s_1).

initial("Existence2",s_0).

accepting("Existence2",s_1).


automaton("Existence3",s_0,a,s_3).
automaton("Existence3",s_1,c,s_1).
automaton("Existence3",s_2,c,s_2).
automaton("Existence3",s_3,c,s_3).
automaton("Existence3",s_2,a,s_2).
automaton("Existence3",s_0,c,s_0).
automaton("Existence3",s_3,a,s_1).
automaton("Existence3",s_1,a,s_2).

initial("Existence3",s_0).

accepting("Existence3",s_2).


automaton("Existence",s_1,c,s_1).
automaton("Existence",s_0,c,s_0).
automaton("Existence",s_1,a,s_1).
automaton("Existence",s_0,a,s_1).

initial("Existence",s_0).

accepting("Existence",s_1).


automaton("Init",s_1,c,s_1).
automaton("Init",s_2,c,s_2).
automaton("Init",s_2,a,s_2).
automaton("Init",s_0,a,s_1).
automaton("Init",s_1,a,s_1).
automaton("Init",s_0,c,s_2).

initial("Init",s_0).

accepting("Init",s_1).


automaton("Not_Chain_Precedence",s_1,c,s_1).
automaton("Not_Chain_Precedence",s_2,a,s_2).
automaton("Not_Chain_Precedence",s_0,a,s_2).
automaton("Not_Chain_Precedence",s_0,c,s_0).
automaton("Not_Chain_Precedence",s_1,b,s_1).
automaton("Not_Chain_Precedence",s_0,b,s_0).
automaton("Not_Chain_Precedence",s_2,c,s_0).
automaton("Not_Chain_Precedence",s_2,b,s_1).
automaton("Not_Chain_Precedence",s_1,a,s_1).

initial("Not_Chain_Precedence",s_0).

accepting("Not_Chain_Precedence",s_0).
accepting("Not_Chain_Precedence",s_2).


automaton("Not_Chain_Response",s_1,c,s_1).
automaton("Not_Chain_Response",s_2,a,s_2).
automaton("Not_Chain_Response",s_0,a,s_2).
automaton("Not_Chain_Response",s_0,c,s_0).
automaton("Not_Chain_Response",s_1,b,s_1).
automaton("Not_Chain_Response",s_0,b,s_0).
automaton("Not_Chain_Response",s_2,c,s_0).
automaton("Not_Chain_Response",s_2,b,s_1).
automaton("Not_Chain_Response",s_1,a,s_1).

initial("Not_Chain_Response",s_0).

accepting("Not_Chain_Response",s_0).
accepting("Not_Chain_Response",s_2).


automaton("Not_Chain_Succession",s_1,c,s_1).
automaton("Not_Chain_Succession",s_2,a,s_2).
automaton("Not_Chain_Succession",s_0,a,s_2).
automaton("Not_Chain_Succession",s_0,c,s_0).
automaton("Not_Chain_Succession",s_1,b,s_1).
automaton("Not_Chain_Succession",s_0,b,s_0).
automaton("Not_Chain_Succession",s_2,c,s_0).
automaton("Not_Chain_Succession",s_2,b,s_1).
automaton("Not_Chain_Succession",s_1,a,s_1).

initial("Not_Chain_Succession",s_0).

accepting("Not_Chain_Succession",s_0).
accepting("Not_Chain_Succession",s_2).


automaton("Not_CoExistence",s_0,a,s_3).
automaton("Not_CoExistence",s_1,c,s_1).
automaton("Not_CoExistence",s_2,c,s_2).
automaton("Not_CoExistence",s_3,b,s_1).
automaton("Not_CoExistence",s_3,c,s_3).
automaton("Not_CoExistence",s_2,b,s_2).
automaton("Not_CoExistence",s_0,c,s_0).
automaton("Not_CoExistence",s_1,b,s_1).
automaton("Not_CoExistence",s_2,a,s_1).
automaton("Not_CoExistence",s_1,a,s_1).
automaton("Not_CoExistence",s_3,a,s_3).
automaton("Not_CoExistence",s_0,b,s_2).

initial("Not_CoExistence",s_0).

accepting("Not_CoExistence",s_0).
accepting("Not_CoExistence",s_2).
accepting("Not_CoExistence",s_3).


automaton("Not_Precedence",s_1,c,s_1).
automaton("Not_Precedence",s_2,c,s_2).
automaton("Not_Precedence",s_1,b,s_2).
automaton("Not_Precedence",s_2,a,s_2).
automaton("Not_Precedence",s_2,b,s_2).
automaton("Not_Precedence",s_0,c,s_0).
automaton("Not_Precedence",s_0,b,s_0).
automaton("Not_Precedence",s_0,a,s_1).
automaton("Not_Precedence",s_1,a,s_1).

initial("Not_Precedence",s_0).

accepting("Not_Precedence",s_0).
accepting("Not_Precedence",s_1).


automaton("Not_Responded_Existence",s_0,a,s_3).
automaton("Not_Responded_Existence",s_1,c,s_1).
automaton("Not_Responded_Existence",s_2,c,s_2).
automaton("Not_Responded_Existence",s_3,b,s_1).
automaton("Not_Responded_Existence",s_3,c,s_3).
automaton("Not_Responded_Existence",s_2,b,s_2).
automaton("Not_Responded_Existence",s_0,c,s_0).
automaton("Not_Responded_Existence",s_1,b,s_1).
automaton("Not_Responded_Existence",s_2,a,s_1).
automaton("Not_Responded_Existence",s_1,a,s_1).
automaton("Not_Responded_Existence",s_3,a,s_3).
automaton("Not_Responded_Existence",s_0,b,s_2).

initial("Not_Responded_Existence",s_0).

accepting("Not_Responded_Existence",s_0).
accepting("Not_Responded_Existence",s_2).
accepting("Not_Responded_Existence",s_3).


automaton("Not_Response",s_1,c,s_1).
automaton("Not_Response",s_2,c,s_2).
automaton("Not_Response",s_1,b,s_2).
automaton("Not_Response",s_2,a,s_2).
automaton("Not_Response",s_2,b,s_2).
automaton("Not_Response",s_0,c,s_0).
automaton("Not_Response",s_0,b,s_0).
automaton("Not_Response",s_0,a,s_1).
automaton("Not_Response",s_1,a,s_1).

initial("Not_Response",s_0).

accepting("Not_Response",s_0).
accepting("Not_Response",s_1).


automaton("Not_Succession",s_1,c,s_1).
automaton("Not_Succession",s_2,c,s_2).
automaton("Not_Succession",s_1,b,s_2).
automaton("Not_Succession",s_2,a,s_2).
automaton("Not_Succession",s_2,b,s_2).
automaton("Not_Succession",s_0,c,s_0).
automaton("Not_Succession",s_0,b,s_0).
automaton("Not_Succession",s_0,a,s_1).
automaton("Not_Succession",s_1,a,s_1).

initial("Not_Succession",s_0).

accepting("Not_Succession",s_0).
accepting("Not_Succession",s_1).


automaton("Precedence",s_1,c,s_1).
automaton("Precedence",s_2,c,s_2).
automaton("Precedence",s_0,b,s_1).
automaton("Precedence",s_2,a,s_2).
automaton("Precedence",s_2,b,s_2).
automaton("Precedence",s_0,a,s_2).
automaton("Precedence",s_0,c,s_0).
automaton("Precedence",s_1,b,s_1).
automaton("Precedence",s_1,a,s_1).

initial("Precedence",s_0).

accepting("Precedence",s_0).
accepting("Precedence",s_2).


automaton("Responded_Existence",s_1,c,s_1).
automaton("Responded_Existence",s_2,c,s_2).
automaton("Responded_Existence",s_0,b,s_1).
automaton("Responded_Existence",s_2,a,s_2).
automaton("Responded_Existence",s_0,a,s_2).
automaton("Responded_Existence",s_0,c,s_0).
automaton("Responded_Existence",s_1,b,s_1).
automaton("Responded_Existence",s_2,b,s_1).
automaton("Responded_Existence",s_1,a,s_1).

initial("Responded_Existence",s_0).

accepting("Responded_Existence",s_0).
accepting("Responded_Existence",s_1).


automaton("Response",s_1,c,s_1).
automaton("Response",s_0,c,s_0).
automaton("Response",s_0,b,s_0).
automaton("Response",s_0,a,s_1).
automaton("Response",s_1,b,s_0).
automaton("Response",s_1,a,s_1).

initial("Response",s_0).

accepting("Response",s_0).


automaton("Succession",s_0,a,s_3).
automaton("Succession",s_1,c,s_1).
automaton("Succession",s_2,c,s_2).
automaton("Succession",s_3,b,s_1).
automaton("Succession",s_3,c,s_3).
automaton("Succession",s_2,a,s_2).
automaton("Succession",s_2,b,s_2).
automaton("Succession",s_1,a,s_3).
automaton("Succession",s_0,c,s_0).
automaton("Succession",s_1,b,s_1).
automaton("Succession",s_3,a,s_3).
automaton("Succession",s_0,b,s_2).

initial("Succession",s_0).

accepting("Succession",s_0).
accepting("Succession",s_1).


