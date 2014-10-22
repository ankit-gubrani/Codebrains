<%--

  Multifield Demo Component component.

  This is demo component to show custom xtypes usage with out of the box multifield.

--%><%
%>
<%@include file="/libs/foundation/global.jsp" %>
<%
%>
<%@page session="false" %>

<strong>Multifield Demo Component component.</strong>
<br>
<u>Here are the paths read from custom Multifield : </u><br>
<c:forEach items="${properties.multifield}" var="path">
    ${path}
    <br>
</c:forEach>

