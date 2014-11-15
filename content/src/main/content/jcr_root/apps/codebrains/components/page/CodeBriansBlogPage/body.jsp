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

  Blog: Body script (included by page.jsp)

  ==============================================================================

--%><%@page session="false" %><%@include file="/libs/foundation/global.jsp" %><%

%><body>
<cq:include path="clientcontext" resourceType="cq/personalization/components/clientcontext"/>
<div id="page">
    <cq:include path="header" resourceType="codebrains/components/content/social/header" />
    <cq:include script="content.jsp"/>
    <cq:include path="footer" resourceType="social/blog/components/footer" />
</div>
<cq:include path="cloudservices" resourceType="cq/cloudserviceconfigs/components/servicecomponents"/>
</body>
