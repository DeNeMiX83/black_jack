ifeq ($(ENV),prod)
include deploy/Makefile.prod
else ifeq ($(ENV),dev)
include deploy/Makefile.dev
else
$(error Invalid value for ENV variable: $(ENV))
endif