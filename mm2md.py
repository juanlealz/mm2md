#!/usr/bin/env python
# -*- coding: UTF8 -*-

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
	if "bullets" in icons:
		next_bullet="-"
	elif "numbers" in icons:
		next_bullet="1."
	else:
		next_bullet=None
	if "multi-node_paragraph" in icons:
		next_multinode_paragraph=True
	else:
		next_multinode_paragraph=False
		
	#document title
	if header_depth==0:
		print "---"
		print "title: ",
		print e.attrib.get("TEXT").encode('UTF8')
		print "...\n"
		for node in e.findall("node"):
			print_node(node, header_depth+1, multinode_paragraph=next_multinode_paragraph)

	#comments
	elif "comments" in icons:
		pass
	elif "comment" in icons:
		for node in e.findall("node"):
			print_node(node, header_depth, bullet, bullet_depth, multinode_paragraph=next_multinode_paragraph)
		if "multi-node_paragraph" in icons and not multinode_paragraph:
			print "\n\n",			

	#heading
	elif "heading" in icons:
		print "#"*header_depth,
		print e.attrib.get("TEXT").encode('UTF8'),
		print "\n\n",
		for node in e.findall("node"):
			print_node(node, header_depth+1, bullet=next_bullet, bullet_depth=bullet_depth, multinode_paragraph=next_multinode_paragraph)

	#bullet-list start
	elif bullet is None and ("bullets" in icons or "numbers" in icons):
		print e.attrib.get("TEXT").encode('UTF8'),
		print "\n\n",
		for node in e.findall("node"):
			print_node(node, header_depth, bullet=next_bullet, bullet_depth=bullet_depth, multinode_paragraph=next_multinode_paragraph)
		print "\n",
		
	#bullet-list item
	elif bullet is not None:
		print "    "*bullet_depth+bullet,
		if e.attrib.get("TEXT") is None:
			print ""
		else:
			print e.attrib.get("TEXT").encode('UTF8'),
		if not "multi-node_paragraph" in icons:
			print "\n",
		if next_bullet is None and not "multi-node_paragraph" in icons:
			next_bullet="-"
		for node in e.findall("node"):
			print_node(node, header_depth, bullet=next_bullet, bullet_depth=bullet_depth+1, multinode_paragraph=next_multinode_paragraph)
		if "multi-node_paragraph" in icons:
			print "\n",
		
	#multi-node paragraph header
	elif "multi-node_paragraph" in icons:
		print e.attrib.get("TEXT").encode('UTF8'),
		print " ",
		for node in e.findall("node"):
			print_node(node, header_depth, bullet=next_bullet, bullet_depth=bullet_depth, multinode_paragraph=next_multinode_paragraph)
		if not multinode_paragraph:
			print "\n\n",
	
	#multi-node paragraph item
	elif multinode_paragraph:
		print e.attrib.get("TEXT").encode('UTF8'),
		for node in e.findall("node"):
			print_node(node, header_depth, bullet=None, bullet_depth=bullet_depth, multinode_paragraph=True)
		
	#implicit bullet-list start
	elif e.find("node") is not None:
		next_bullet="-"
		print e.attrib.get("TEXT").encode('UTF8'),
		print "\n\n",
		for node in e.findall("node"):
			print_node(node, header_depth, bullet=next_bullet, bullet_depth=bullet_depth, multinode_paragraph=next_multinode_paragraph)
		print "\n",
		return

	#one-node paragraph
	else:
		print e.attrib.get("TEXT").encode('UTF8'),
		print "\n\n",
	
#Start	
et = ElementTree.parse(argv[1])
print_node(et.find("node"))