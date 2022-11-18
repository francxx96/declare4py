

class ALPEncoding(str):
    value: str = """time(1..t). %t = lunghezza traccia

cur_state(I,S,0) :- initial(Name,S),template(I,Name).

{trace(A,T) : activity(A)} = 1 :- time(T).
{assigned_value(K,V,T) : value(K,V)} = 1 :- trace(A,T), has_attribute(A,K).


cur_state(I,S2,T) :- cur_state(I,S1,T-1), template(I,Name), automaton(Name,S1,c,S2), trace(A,T), not activation(I,A), not target(I,A).
cur_state(I,S2,T) :- cur_state(I,S1,T-1), template(I,Name), automaton(Name,S1,c,S2), trace(A,T), activation(I,A), not activation_condition(I,T).
cur_state(I,S2,T) :- cur_state(I,S1,T-1), template(I,Name), automaton(Name,S1,a,S2), trace(A,T), activation(I,A), activation_condition(I,T).
cur_state(I,S2,T) :- cur_state(I,S1,T-1), template(I,Name), automaton(Name,S1,c,S2), trace(A,T), target(I,A), not correlation_condition(I,T).
cur_state(I,S2,T) :- cur_state(I,S1,T-1), template(I,Name), automaton(Name,S1,b,S2), trace(A,T), target(I,A), correlation_condition(I,T).


sat(I,T) :- cur_state(I,S,T), template(I,Name), accepting(Name,S). 

:- template(I,_), not  sat(I,t).

#show trace/2.
#show assigned_value/3.
%#show sat/2."""
