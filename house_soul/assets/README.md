So this iteration makes use of Pico's Porcupine and Rhino services.

The models used for this are generated using their web-based console and
are not usuable without a valid token. However, the verbiage in the license either
accidently or delibertly seem to indicate the built models are private.

I'm erroring on the side of caution, and am considering them "secrets" in the
same way my token is.

What I _can_ do is include the .yaml for the Rhino library and instructions for
building the wake-command yourself using their system.

Of course, the "stormlight.yml" being here isn't really correct, since THAT should
be a plugin. TODO is sort that out once I figure out the plugin mechs

