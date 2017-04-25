Background
- we need to write a collaborative project with scientific aims
- most of us are interested in: data analysis / modelling / simulations / deep networks
- the focus here is on programming, hence the generic aspect of the design, it's tool building!
- that said we have a structured goal: to model the outcome of the federal elections


The basic idea of the project is to
create an architecture similar to that behind the scenes of the politics
modelling engine at https://fivethirtyeight.com/
I want you, as a group, to create a generic engine capable of (i)
storing data (eg political polls), (ii) interpretting a generic
'modelling language' (which we will define ourselves), (iii) running the
model described by the modelling language, probably involving
monte-carlo runs of the outputs, and (iv) producing predicted outputs
for the future behaviour of the system. Our test system will be the
German federal elections, which will take place at the end of the
summer. Polls should be appearing online throughout the summer. We will
try to predict the election outcome based on these polls. The important
thing to note is that, success is not dictated by how good our model is
but rather how generic our architecture is. I can create a model on my
own. I want a modelling system.
