%import energenie

<H1>Registered devices</H1>

<form method=get>
<table border=1 cellspacing=1 cellpadding=5>
%for name in names:
  %c = energenie.registry.peek(name)

  <tr><td>{{name}}</td>

  %if c.can_send():
    <td><input type="button" value="watch"> <input type="button" value="un-watch"></td>
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
    <td><input type="button" value="on"> <input type="button" value="off"></td>
  %else:
    <td>&nbsp;</td>
  %end

  <td><input type="button" value="rename"> <input type="text"></td>
  <td><input type="button" value="delete"></td>

%end
</table>
</form>

