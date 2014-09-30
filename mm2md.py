#!/usr/bin/env python
# -*- coding: latin-1 -*-

from xml.etree import ElementTree
from sys import argv

# Recursive		 
def print_node (e, header_depth=0, bullet=None, bullet_depth=0, multinode_paragraph=False):
	#parse icons
	icons=[]
	for icon in e.findall("icon"):
		icons.append(icon.attrib.get("BUILTIN"))
	icons=set(icons)

	#multi-node paragraph and bullets
	next_bullet=None
	if "numbers" in icons:
		next_bullet="1."
	if "bullets" in icons:
		next_bullet="-"
	if "multi-node_paragraph" in icons:
		next_multinode_paragraph=True
	else:
		next_multinode_paragraph=False
		
	#document title
	if header_depth==0:
		print "---"
		print "title: ",
		print e.attrib.get("TEXT").encode('latin-1')
		print "...\n"
		for node in e.findall("node"):
			print_node(node, header_depth+1, multinode_paragraph=next_multinode_paragraph)
		return

	#comments
	if "comments" in icons:
		return
	if "comment" in icons:
		for node in e.findall("node"):
			print_node(node, header_depth, bullet, bullet_depth, multinode_paragraph=next_multinode_paragraph)
		if "multi-node_paragraph" in icons and not multinode_paragraph:
			print "\n\n",			
		return

	#heading
	if "heading" in icons:
		print "#"*header_depth,
		print e.attrib.get("TEXT").encode('latin-1'),
		print "\n\n",
		for node in e.findall("node"):
			print_node(node, header_depth+1, bullet=next_bullet, bullet_depth=bullet_depth, multinode_paragraph=next_multinode_paragraph)
		return

	#bullet-list start
	if bullet is None and ("bullets" in icons or "numbers" in icons):
		print e.attrib.get("TEXT").encode('latin-1'),
		print "\n\n",
		for node in e.findall("node"):
			print_node(node, header_depth, bullet=next_bullet, bullet_depth=bullet_depth, multinode_paragraph=next_multinode_paragraph)
		print "\n",
		return
		
	#bullet-list item
	if bullet is not None:
		print "    "*bullet_depth+bullet,
		print e.attrib.get("TEXT").encode('latin-1'),
		if not "multi-node_paragraph" in icons:
			print "\n",
		if next_bullet is None and not "multi-node_paragraph" in icons:
			next_bullet="-"
		for node in e.findall("node"):
			print_node(node, header_depth, bullet=next_bullet, bullet_depth=bullet_depth+1, multinode_paragraph=next_multinode_paragraph)
		if "multi-node_paragraph" in icons:
			print "\n",
		return
		
	#multi-node paragraph header
	if "multi-node_paragraph" in icons:
		print e.attrib.get("TEXT").encode('latin-1'),
		print " ",
		for node in e.findall("node"):
			print_node(node, header_depth, bullet=next_bullet, bullet_depth=bullet_depth, multinode_paragraph=next_multinode_paragraph)
		if not multinode_paragraph:
			print "\n\n",
		return		
	
	#multi-node paragraph item
	if multinode_paragraph:
		print e.attrib.get("TEXT").encode('latin-1'),
		for node in e.findall("node"):
			print_node(node, header_depth, bullet=None, bullet_depth=bullet_depth, multinode_paragraph=True)
		return
		
	#implicit bullet-list start
	if e.find("node") is not None:
		next_bullet="-"
		print e.attrib.get("TEXT").encode('latin-1'),
		print "\n\n",
		for node in e.findall("node"):
			print_node(node, header_depth, bullet=next_bullet, bullet_depth=bullet_depth, multinode_paragraph=next_multinode_paragraph)
		print "\n",
		return

	#one-node paragraph
	print e.attrib.get("TEXT").encode('latin-1'),
	print "\n\n",
	
#Start	
et = ElementTree.parse(argv[1])
print_node(et.find("node"))
#for n in et.find(".//node"):
#	print_node(n)