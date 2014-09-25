#!/usr/bin/env python
# -*- coding: latin-1 -*-

from xml.etree import ElementTree
from sys import argv

# Recursive		 
def print_node (e, header_depth=0, bullet=None, bullet_depth=0, parent_icons=None):
	#parse icons
	icons=[]
	for icon in e.findall("icon"):
		icons.append(icon.attrib.get("BUILTIN"))
	icons=set(icons)
	
	#document title
	if header_depth==0:
		print "---"
		print "title: ",
		print e.attrib.get("TEXT").encode('latin-1')
		print "...\n"
		for node in e.findall("node"):
			print_node(node, header_depth+1, parent_icons=icons)
		return

	#comments
	if "comments" in icons:
		return
	if "comment" in icons:
		for node in e.findall("node"):
			print_node(node, header_depth, bullet, bullet_depth, parent_icons)
		return
	
	#prefix
	if "heading" in icons:
		print "#"*header_depth,
	if bullet is not None:
		print "    "*bullet_depth+bullet,
		bullet_depth += 1

	#text
	print e.attrib.get("TEXT").encode('latin-1'),

	#newlines
	# - 2 when it is a header
	# - 2 when it is a normal paragraph
	# - 1 when it is a bullet list item
	# - 0 when it is part of a multi-node paragraph
	if "page_white_text" in icons or "page_white_text" in parent_icons:
		print " ",
	elif bullet is not None:
		print "\n",
	else:
		print "\n\n",
		
	#prepare recursion
	next_bullet="-"
	if "numbers" in icons:
		next_bullet="1."
	if "heading" in icons:
		header_depth +=1
		next_bullet=None
	if "page_white_text" in icons:
		next_bullet=bullet
		
	#recurse
	for node in e.findall("node"):
		print_node(node, header_depth, next_bullet, bullet_depth, parent_icons)
	
	#after subtree
	# - 1 when it is a first-level bullet list header (has children)  
	if bullet_depth==0 and bullet is None and next_bullet is not None:
		print "\n",

#Start	
et = ElementTree.parse(argv[1])
print_node(et.find("node"))
#for n in et.find(".//node"):
#	print_node(n)