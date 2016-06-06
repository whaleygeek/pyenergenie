<html>
<body>
<script type="text/javascript">
function do_action(action)
{
  document.myform.action=action
  document.myform.submit()
}

function do_rename(old_name)
{
  new_name = prompt("What do you want to rename " + old_name + " to?", old_name)
  if (new_name != null)
  {
    do_action("/rename_device/" + old_name + "/" + new_name)
  }
}

function do_delete(name)
{
  y = prompt("really delete " + name + "?")
  if (y != null)
  {
    do_action("/delete_device/" + name)
  }
}
</script>


%import energenie
%c = energenie.registry.peek(name)
%label = str(c)

<H1>Device details: {{name}}</H1>
Type: {{label}}<BR>

<form name="myform" method=get>
  <button type="button" onclick="do_rename('{{name}}')">Rename</button>
  <button type="button" onclick="do_delete('{{name}}')">Delete</button>
</form>

</html>
</body>
