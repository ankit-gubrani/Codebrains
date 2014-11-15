<%--

 ADOBE CONFIDENTIAL
 __________________

  Copyright 2011 Adobe Systems Incorporated
  All Rights Reserved.

 NOTICE:  All information contained herein is, and remains
 the property of Adobe Systems Incorporated and its suppliers,
 if any.  The intellectual and technical concepts contained
 herein are proprietary to Adobe Systems Incorporated and its
 suppliers and are protected by trade secret or copyright law.
 Dissemination of this information or reproduction of this material
 is strictly forbidden unless prior written permission is obtained
 from Adobe Systems Incorporated.

  ==============================================================================

  Blog: Content script (included by body.jsp)

  ==============================================================================

--%><%@ page session="false" import="com.adobe.cq.social.blog.Blog,
                     com.adobe.cq.social.blog.BlogManager" %><%
%><%@include file="/libs/foundation/global.jsp" %><%

    BlogManager blogMgr = resource.getResourceResolver().adaptTo(BlogManager.class);
    Blog blog = blogMgr.getBlog(slingRequest);

%><div id="content" class="<%= blog.isEntry() ? "widecolumn" : "narrowcolumn" %>" style="width:70%; display:block; float:left; ">

<cq:include path="blog" resourceType="social/blog/components/main" />

</div>

<%

    if (!blog.isEntry()) {

    %>
<div id="sidebar" style="width:29%; float : left; display:block; ">
        <ul>
            <cq:include path="sidebar" resourceType="foundation/components/iparsys"/>
        </ul>
    </div>
    <%
    }
%>

<div style="clear:both;" ></div>
