activity(activity_1).
has_attribute(activity_1,categorical).
has_attribute(activity_1,integer).

activity(activity_2).
has_attribute(activity_2,categorical).
has_attribute(activity_2,integer).

activity(activity_3).
has_attribute(activity_3,categorical).
has_attribute(activity_3,integer).

activity(activity_4).
has_attribute(activity_4,categorical).
has_attribute(activity_4,integer).

activity(activity_5).
has_attribute(activity_5,categorical).
has_attribute(activity_5,integer).

activity(activity_6).
has_attribute(activity_6,categorical).
has_attribute(activity_6,integer).

activity(activity_7).
has_attribute(activity_7,categorical).
has_attribute(activity_7,integer).

activity(activity_8).
has_attribute(activity_8,categorical).
has_attribute(activity_8,integer).

activity(activity_9).
has_attribute(activity_9,categorical).
has_attribute(activity_9,integer).

activity(activity_10).
has_attribute(activity_10,categorical).
has_attribute(activity_10,integer).

activity(activity_11).
has_attribute(activity_11,categorical).
has_attribute(activity_11,integer).

activity(activity_12).
has_attribute(activity_12,categorical).
has_attribute(activity_12,integer).

activity(activity_13).
has_attribute(activity_13,categorical).
has_attribute(activity_13,integer).

activity(activity_14).
has_attribute(activity_14,categorical).
has_attribute(activity_14,integer).

activity(activity_15).
has_attribute(activity_15,categorical).
has_attribute(activity_15,integer).

activity(activity_16).
has_attribute(activity_16,categorical).
has_attribute(activity_16,integer).

activity(activity_17).
has_attribute(activity_17,categorical).
has_attribute(activity_17,integer).

value(integer,0..100).

value(categorical,c1).
value(categorical,c2).
value(categorical,c3).

template(0,"Response").
activation(0,activity_1).
activation_condition(0,T) :- assigned_value(integer,V,T),V>10.
target(0,activity_2).
correlation_condition(0,T) :- assigned_value(integer,V,T),V>10.

template(1,"Chain Response").
activation(1,activity_3).
activation_condition(1,T) :- assigned_value(categorical,c1,T).
target(1,activity_4).
correlation_condition(1,T) :- assigned_value(categorical,c2,T).

template(2,"Absence").
activation(2,activity_5).
activation_condition(2,T) :- assigned_value(categorical,c3,T).

template(3,"Response").
activation(3,activity_6).
activation_condition(3,T) :- assigned_value(integer,V,T),V>10.
target(3,activity_7).
correlation_condition(3,T) :- assigned_value(integer,V,T),V>10.

template(4,"Chain Response").
activation(4,activity_8).
activation_condition(4,T) :- assigned_value(categorical,c1,T).
target(4,activity_9).
correlation_condition(4,T) :- assigned_value(categorical,c2,T).

template(5,"Existence").
activation(5,activity_10).
activation_condition(5,T) :- assigned_value(categorical,c3,T).

template(6,"Response").
activation(6,activity_11).
activation_condition(6,T) :- assigned_value(integer,V,T),V>10.
target(6,activity_12).
correlation_condition(6,T) :- assigned_value(integer,V,T),V>10.

template(7,"Chain Response").
activation(7,activity_13).
activation_condition(7,T) :- assigned_value(categorical,c1,T).
target(7,activity_14).
correlation_condition(7,T) :- assigned_value(categorical,c2,T).

template(8,"Existence").
activation(8,activity_15).
activation_condition(8,T) :- assigned_value(categorical,c3,T).

template(9,"Response").
activation(9,activity_16).
activation_condition(9,T) :- assigned_value(integer,V,T),V>10.
target(9,activity_17).
correlation_condition(9,T) :- assigned_value(integer,V,T),V>10.

