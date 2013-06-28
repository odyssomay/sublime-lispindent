sublime-lispindent is a plugin for [sublime text 2](http://www.sublimetext.com/)
that properly indents lisp code.

## Installation

### With package control (recommended)

Use [Sublime Package Control](http://wbond.net/sublime_packages/package_control),
the package is called `lispindent`.

### Manually

1. Clone the repository or download the [zipfile](https://github.com/odyssomay/sublime-lispindent/archive/master.zip).
2. The resulting folder - either from cloning or unzipping - should be moved to
`Installed Packages` inside your data folder.

The location of the data folder varies between systems:

 * *Linux* - `~/.config/sublime-text-2`
 * *OSX* - `~/Library/Application Support/Sublime Text 2`
 * *Windows* - `%APPDATA%\Sublime Text 2`

## Supported languages

<table>
	<tr><td>clojure</td><td>.clj, .cljs, .edn</td></tr>
	<tr><td>common lisp</td><td>.lsp, .lisp</td></tr>
	<tr><td>racket</td><td>.rkt, .rktd, .rktl</td></tr>
	<tr><td>scheme</td><td>.ss, .scm, .sch</td></tr>
</table>

If your language is not one of the above,
open an issue or contact [me](https://github.com/odyssomay)
to get it included.

You can also add your own language or change the existing configurations
in the menu `Preferences->Lispindent->Settings`.

For a minimal configuration that should work fine for most
languages, I recommend the following:

```json
"<language-name>": {
	"detect": ".*\\.(<file-endings>)$",
	"default_indent": "two_space",
	"regex": "$"
}
```

Replace `<language-name>` with the name of your language.
It does not matter what you write here, as long as it is distinct from
the other languages.

Replace `<file-endings>` with the possible file endings for your language.
Note: without the dot!
Delimit endings with `|`.
Example: `lsp|lisp` for common lisp.

## Key bindings

<table>
	<tr>
		<td>enter</td>
		<td>Insert a new line with indentation</td>
	</tr>
	<tr>
		<td>ctrl+i or<br/>cmd+i (osx)</td>
		<td>Indent selected lines (or the current line, if there is no selection).</td>
	</tr>
</table>

To change key bindings, open the menu `Preferences->Lispindent`.
Select `Key Bindings – Default` for windows/linux, or
`Key Bindings – OSX` for mac.

## License

sublime-lispindent is licensed under the [zlib](http://en.wikipedia.org/wiki/Zlib_license) license:

---

Copyright (c) 2012 Jonathan Fischer Friberg

This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose, including commercial applications, and to alter it and redistribute it freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not claim that you wrote the original software. If you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not required.

2. Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.

3. This notice may not be removed or altered from any source distribution.
