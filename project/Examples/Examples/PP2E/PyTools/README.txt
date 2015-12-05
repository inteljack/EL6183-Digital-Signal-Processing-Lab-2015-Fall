A package of tools used to maintain book example 
distribution; many are examples in the book as well.

See also related examples in:

- PP2E\System\Filetools directory (compare and copy 
  directories, etc.)

- PP2E\Internet\Cgi-Web directory (install CGI scripts,
  change site names in all web example files)

- etc.

The name PyTools is used here because the module seach
path already included a "Tools" in the Gui directory when
I first set the tree up.  Since then, all imports are made
through the PP2E root directory, so there is no reason that
this need have a "Py" at the front.  That is, the following
two imports would be distinct:

import PP2E.Tools
import PP2E.Gui.Tools

But I like the "Py" now that I've gotten used to it.

