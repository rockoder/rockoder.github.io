---
layout: post
title: 'Copy VS Code Markdown Color Highlighting to Sublime Text for Solarized (Light) Color Scheme'
date: '2020-04-26'
author: rockoder
tags:
- hacking, productivity
---

Sublime Text is my go to text editor. However, I recently ended up using Visual Studio Code and was really impressed by the syntax highlights for Markdown file in the Solarized (Light) Color Scheme.

Since all my configurations, customizations and extensions are set in Sublime Text, it would be a non-trivial job to switch the editor. But I missed the syntax highlights of Visual Studio Code and wished if I could apply the same in the Sublime Text.

I could not find any easy extension to do this. Finally, I ended up modifying the Solarized file. Here are the steps I followed. Hope this helps somebody.

1. Go to Preferences -> Browse Packages... Menu. This should take you to the directory where all the packages for the Sublime Text are stored.
1. Copy the `Solarized Color Scheme.sublime-package` to some temporary location say ~/temp/.
1. Rename ~/temp/Solarized Color Scheme.sublime-package to ~/temp/Solarized Color Scheme.zip
1. Uncompress the zip file
1. Go inside the uncompressed directory
1. Make following changes/additions in the file `Solarized (light).sublime-color-scheme`:
```json
		{
            "scope": "entity.name.section",
            "foreground": "var(blue)"
        },
		{
            "scope": "markup.heading, punctuation.definition.heading.markdown",
            "foreground": "var(blue)",
            "font_style": "bold"
        },
        {
            "scope": "markup.list.unnumbered.markdown, markup.list.unnumbered.bullet.markdown, markup.list.numbered.markdown, markup.list.numbered.bullet.markdown",
            "foreground": "var(yellow)",
        },
        {
            "name": "Markdown em",
            "scope": "markup.italic",
            "font_style": "italic",
            "foreground": "var(magenta)"
        },
        {
            "scope": "markup.bold",
            "font_style": "bold",
            "foreground": "var(magenta)"
        },
```
1. Zip the directory.
1. Rename ~/temp/Solarized Color Scheme.zip to ~/temp/Solarized Color Scheme.sublime-package
1. Copy ~/temp/Solarized Color Scheme.sublime-package to the original location
1. Restart Sublime Text

This may not cover advance Markdown parsing and syntax highlighting. But this was sufficient for me to continue using Sublime Text.

This delayed my switch to Visual Studio Code. For now.