import unittest

from main import *
from htmlnode import *

class testMain(unittest.TestCase):
    maxDiff = None
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
- this is an unordered list
- another one
- and another
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is an unordered list</li><li>another one</li><li>and another</li></ul></div>"
        )
    
    def test_ordered_list(self):
        md = """
1. this is an ordered list
2. another item
3. and another
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is an ordered list</li><li>another item</li><li>and another</li></ol></div>"
        )
    
    def test_heading(self):
        md = """
# first test_heading
## second test heading
### third test_heading
#### fourth test_heading
##### fifth test heading
###### last test heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>first test_heading</h1><h2>second test heading</h2><h3>third test_heading</h3><h4>fourth test_heading</h4><h5>fifth test heading</h5><h6>last test heading</h6></div>"
        )
    
    def test_quote(self):
        md = """
# this heading is for test_quote
> quote of the day

> another quote with _italic_ and **bold**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this heading is for test_quote</h1><blockquote>quote of the day</blockquote><blockquote>another quote with <i>italic</i> and <b>bold</b></blockquote></div>"
        )
    
    def test_heading_new(self):
        md = """
#this is not a heading
######## will this be a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>#this is not a heading ######## will this be a heading</p></div>"
        )

    def test_mixed_block(self):
        md = """
# The blind rat

The blind rat ate a trapped cheese.
The blind rat got caught in the mouse trap.

Lesson of the day:
- do not take free meals
- watch your surrounding

Always be wary of your surrounding and 
make sure to watch your step.

Steps to take:
1. always be closing
2. look into the horizon

> Failure is not the opposite of success; it's part of success

```
code block check
with new line please
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,

            "<div><h1>The blind rat</h1><p>The blind rat ate a trapped cheese.The blind rat got caught in the mouse trap.</p><p>Lesson of the day:</p><ul><li>do not take free meals</li><li>watch your surrounding</li></ul><p>Always be wary of your surrounding and make sure to watch your step.</p><p>Steps to take:</p><ol><li>always be closing</li><li>look into the horizon</li></ol><blockquote>Failure is not the opposite of success; it's part of success</blockquote><pre><code>code block check\nwith new line please\n</code></pre></div>"
        )
