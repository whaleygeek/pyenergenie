<html>
<head>
<script type="text/javascript">
function do_action(action)
{
  document.myform.action=action
  document.myform.submit()
}

function poll()
{
  // fetch the receive_loop in 1 seconds time
  // it will return a redirect back to here
  function do_loop()
  {
    // leave action unchanged, just refreshes the page as is
    document.myform.submit()
  }
  t = setTimeout(do_loop, 1000)
}
</script>

<body onload="poll()">


%import energenie

<H1>Registered devices</H1>

<button type='button' onclick='do_action("/discovery/none")'>no discovery</button>
<button type='button' onclick='do_action("/discovery/auto")'>auto discovery</button>
<button type='button' onclick='do_action("/discovery/autojoin")'>autojoin discovery</button>
<BR><BR>

<form name="myform" method=get>
<table border=1 cellspacing=1 cellpadding=5>
%for name in names:
  %c = energenie.registry.peek(name)

  <tr>
    <td><a href="/edit/{{name}}">{{name}}</td>

  %if c.has_switch():
    <td>
      <button type='button' onclick="do_action('/switch_device/{{name}}/ON')">on</button>
      <button type='button' onclick="do_action('/switch_device/{{name}}/OFF')">off</button>
    </td>
  %else:
    <td>&nbsp;</td>
  %end

  %if c.can_send():
    <td>
    %if name in readings:
      {{readings[name]}}
    %else:
      &nbsp;
    %end
    </td>
  %else:
    <td>&nbsp;</td>
  %end
%end
</table>
<BR>

<button type='button' onclick="do_action('/log/download')">download log</button>
<button type='button' onclick="do_action('/log/clear')">clear log</button>
<BR><BR>

Recent messages:<BR>
<textarea rows=4 cols=80>
%for msg in messages:
    {{msg}}
%end
</textarea>
</form>


</body></html>
