# -------------------------------------------------------
# this is my csh startup file, ~/.cshrc;  your mileage 
# (and default shell) may vary, but you'll want to apply
# setup-pp.csh's settings for the examples distribution
# -------------------------------------------------------

#########################
# Python-related stuff
#########################

# setup system and module search paths
source /home/mark/PP2ndEd/examples/PP2E/Config/setup-pp.csh

# to run programs and unix executable scripts in current dir
set path = (. $path)

# to run a custom build (unless you've done 'make install')
setenv MYPY /home/mark/python1.5.2-ddjcd/Python-1.5.2
setenv PATH $MYPY:$PATH

# you may also need to run the source below for some of the
# examples which embed Python in C; see this file for details
# source $PP2EHOME/PP2E/Config/setup-pp-embed.csh

#########################
# other non-Python stuff
#########################

source ~/.cshrc-other
