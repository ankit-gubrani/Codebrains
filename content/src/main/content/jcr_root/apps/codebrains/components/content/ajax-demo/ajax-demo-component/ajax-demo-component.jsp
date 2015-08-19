<%--

  Ajaxified-demo Component component.

  This is a Ajaxified component for Ajax Demo


--%><%
%>
<%@include file="/apps/codebrains/global.jsp" %>
<%
%>
<%@page session="false" %>
<div id="${currentNode.identifier}" class="reload-id" ajaxified-component-path="${currentNode.path}">
    This is the ajaxified compnent. This will be reloaded on Click of <b><i>Reload Button </i></b>.
    <br>
    <b>Reload Param -- </b>
    <i>
        <c:choose>
            <c:when test="${empty param.reloadParam}">
                This component has not been reloaded Yet !!!
            </c:when>
            <c:otherwise>
                ${param.reloadParam}
            </c:otherwise>
        </c:choose>
    </i>
</div>