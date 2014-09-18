<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" indent="no" encoding="ISO-8859-1"/>
  <xsl:strip-space elements="*"/>
  <xsl:key name="refid" match="node" use="@ID"/>

<xsl:variable name="tab" select="'    '"/>

<!-- Ignore subtree comments -->
<xsl:template match="node[@COLOR='#cc6600']">
</xsl:template>

<!-- Ignore single-node comments -->
<xsl:template match="node[@COLOR='#a6a6a6']">
    <xsl:apply-templates/>
</xsl:template>

<!-- Document title -->
<xsl:template match="/map/node">
    <xsl:text>---
title: </xsl:text>
    <xsl:value-of select="@TEXT"/>
    <xsl:text>
...

</xsl:text>
    <xsl:apply-templates/>
</xsl:template>

<!-- Headers -->
<xsl:template match="node[@COLOR='#000001']">
    <xsl:for-each select="ancestor::node()/attribute::COLOR">
        <xsl:if test=".='#000001'">
            <xsl:text>#</xsl:text>
        </xsl:if>
    </xsl:for-each>
    <xsl:text># </xsl:text>
    <xsl:apply-templates select="." mode="text"/>
    <xsl:text>

</xsl:text>
    <!-- Continue processing children-->
    <xsl:apply-templates/>
</xsl:template>

<!-- Bullet lists -->
<xsl:template match="node[@COLOR='#000005']">
    <xsl:apply-templates select="." mode="text"/>
    <xsl:text>

</xsl:text>
    <!-- Continue processing children-->
    <xsl:apply-templates mode="bullet">
         <xsl:with-param name="bullet" select="'- '"/>
    </xsl:apply-templates>
    <xsl:text>
</xsl:text>
</xsl:template>
<xsl:template match="node[@COLOR='#000006']">
    <xsl:apply-templates select="." mode="text"/>
    <xsl:text>

</xsl:text>
    <!-- Continue processing children-->
    <xsl:apply-templates mode="bullet">
         <xsl:with-param name="bullet" select="'1. '"/>
    </xsl:apply-templates>
</xsl:template>
<xsl:template match="node[@COLOR='#000005']" mode="bullet">
    <xsl:param name="indent" />
    <xsl:param name="bullet" />
    <xsl:value-of select="$indent"/>
    <xsl:value-of select="$bullet"/>
    <xsl:apply-templates select="." mode="text"/>
    <xsl:text>
</xsl:text>
    <!-- Continue processing children-->
    <xsl:apply-templates mode="bullet">
         <xsl:with-param name="bullet" select="'- '"/>
         <xsl:with-param name="indent">
              <xsl:copy-of select="$tab"/>
              <xsl:value-of select="$indent"/>
         </xsl:with-param>
    </xsl:apply-templates>
</xsl:template>
<xsl:template match="node[@COLOR='#000006']" mode="bullet">
    <xsl:param name="indent" />
    <xsl:param name="bullet" />
    <xsl:value-of select="$indent"/>
    <xsl:value-of select="$bullet"/>
    <xsl:apply-templates select="." mode="text"/>
    <xsl:text>
</xsl:text>
    <!-- Continue processing children-->
    <xsl:apply-templates mode="bullet">
         <xsl:with-param name="bullet" select="'1. '"/>
         <xsl:with-param name="indent">
              <xsl:copy-of select="$tab"/>
              <xsl:value-of select="$indent"/>
         </xsl:with-param>
    </xsl:apply-templates>
</xsl:template>
<xsl:template match="node" mode="bullet">
    <xsl:param name="indent" />
    <xsl:param name="bullet" />
    <xsl:value-of select="$indent"/>
    <xsl:value-of select="$bullet"/>
    <xsl:apply-templates select="." mode="text"/>
    <xsl:text>
</xsl:text>
    <!-- Continue processing children-->
    <xsl:apply-templates mode="bullet">
         <xsl:with-param name="bullet">
              <xsl:value-of select="$bullet"/>
         </xsl:with-param>
         <xsl:with-param name="indent">
              <xsl:copy-of select="$tab"/>
              <xsl:value-of select="$indent"/>
         </xsl:with-param>
    </xsl:apply-templates>
</xsl:template>

<!-- Default nodes -->
<xsl:template match="node">
    <xsl:apply-templates select="." mode="text"/>
    <xsl:text>

</xsl:text>
    <!-- Continue processing children-->
    <xsl:apply-templates mode="bullet">
         <xsl:with-param name="bullet" select="'- '"/>
    </xsl:apply-templates>
    <xsl:text>
</xsl:text>
</xsl:template>

<!-- Process text inside nodes -->
<xsl:template match="node[@LINK]" mode="text">  
    <xsl:text>[</xsl:text>
    <xsl:value-of select="@TEXT"/>
    <xsl:text>](</xsl:text>
    <xsl:value-of select="@LINK"/>
    <xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="node" mode="text">  
    <!-- Print node text -->
    <xsl:value-of select="@TEXT"/>
</xsl:template>

</xsl:stylesheet>