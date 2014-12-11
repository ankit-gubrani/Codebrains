<%--

  Default Property Demo Component component.

  Demo component to show default value added on dropping a component

--%><%
%><%@include file="/libs/foundation/global.jsp"%><%
%><%@page session="false" %><%
%><%
	// TODO add you code here
%>
<hr>
<center>Default Property Demo Component</center>
<br>
<ul>
    <li><u><i>Reading Default Property named default :</u></i>  ${properties.default} </li>
    <li><u><i>Reading Default Property named Under Node :</u></i>  ${properties["defaultNode/defaultprop"]}</li>
</ul>
<hr>
