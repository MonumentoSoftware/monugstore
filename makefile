ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARG):;@true)

dump_key:
	uv run mgs-dump-key $(ARG)
