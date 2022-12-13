dot_files=demo_locally_reachable.dot \
		  demo_random_transitions.dot \
		  demo_states.dot \
		  demo.dot

plot_files=$(patsubst %.dot, %.jpg, $(dot_files))

all: demo.dat $(plot_files)

demo.dat: demo.py
	@python demo.py > $@

$(plot_files): %.jpg: %.dot
	@dot -Tjpg -o $@ $^

demo.py:
	@../fsm_generator -c5 -t4 --dot-file demo.dot --python-output $@ --demo

.PHONY: clean
clean:
	@${RM} -rf demo.py *.dot *.jpg *.scl
