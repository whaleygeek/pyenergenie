<html>
<head>
<script type="text/javascript">
function do_action(action)
{
  document.myform.action=action
  //form seems to auto-get when you press any button anyway?
}

function poll()
{
  // fetch the receive_loop in 1 seconds time
  // it will return a redirect back to here
  function do_loop()
  {
    document.myform.action = '/receive_loop'
    document.myform.submit()
  }
  t = setTimeout(do_loop, 1000)
}
</script>

<body onload="poll()">


%import energenie

<H1>Registered devices</H1>

<form name="myform" method=get>
<table border=1 cellspacing=1 cellpadding=5>
%for name in names:
  %c = energenie.registry.peek(name)

  <tr>
    <td><a href="/edit/{{name}}">{{name}}</td>

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

%end
</table>
</form>

</body></html>
