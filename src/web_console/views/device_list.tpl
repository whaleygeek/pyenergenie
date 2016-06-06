<html>
<head>
<script type="text/javascript">
function do_action(action)
{
  //alert(action)
  document.myform.action=action
}
</script>

<body>


%import energenie

<H1>Registered devices</H1>

<form name="myform" method=get>
<table border=1 cellspacing=1 cellpadding=5>
%for name in names:
  %c = energenie.registry.peek(name)

  <tr><td>{{name}}</td>

  %if c.can_send():
    <td>
       <button onclick='do_action("/watch_device/{{name}}")'>watch</button>
       <button onclick='do_action("/unwatch_device/{{name}}")'>unwatch</button>
    </td>
    <td>
    %if name in readings:
      {{readings[name]}}
    %else:
      &nbsp;
    %end
    </td>
  %else:
    <td>&nbsp;</td>
    <td>&nbsp;</td>
  %end

  %if c.has_switch():
    <td>
      <button onclick="do_action('/switch_device/{{name}}/ON')">on</button>
      <button onclick="do_action('/switch_device/{{name}}/OFF')">off</button>
    </td>
  %else:
    <td>&nbsp;</td>
  %end

  <td>
    <button onclick="do_action('/rename_device/{{name}}/' + 'NEWNAME')">rename</button>
    <input type="text">
  </td>

  <td>
    <button onclick="do_action('/delete_device/{{name}}')">delete</button>
  </td>

%end
</table>
</form>

</body></html>
