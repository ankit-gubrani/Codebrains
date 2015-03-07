<%--

  Ajax-demo wrapper Component component.

  This is a wrapper component for Ajax Demo


--%><%
%>
<%@include file="/apps/codebrains/global.jsp" %>
<%
%>
<%@page session="false" %>
<%@page import="java.util.*" %>
<%
%><%
    // TODO add you code here
%>
<cq:includeClientLib categories="codebrains.ajax.demo"/>
Codebrains Ajax Demo Wrapper component. <br>
On click of <b><i>Reload Buton </b></i> Ajax-Demo Component will be reloaded on with reloading page via AJAX

<br>

<input type="text" placeholder="Demo Reload Param" class="reload-param" name="reloadParam"/>
<input type="button" class="reload-btn" value="Reload"/>

<c:set var="uuid" value="<%= UUID.randomUUID().toString() %>"/>
<div id="${uuid}" style="clear:both"></div>

<cq:include path="wapper-par" resourceType="foundation/components/parsys"/>

<div style="text-align:center"><b>~~~~~Codebrains~~~~~</b></div>
<script type="text/javascript">
    $(document).ready(function () {
        $('#${uuid}').closest('.ajax-demo-wrapper').wrapper();
    });
</script>