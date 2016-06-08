<H1>Learn legacy devices</H1>

<script type='text/javascript'>
function do_on()
{
    house_code = document.myform.house_code.value
    if (house_code == "")
    {
        house_code = '6C6C6'
    }
    device_index = document.myform.device_index.value

    document.myform.action = '/legacy_learn/on/' + house_code + '/' + device_index
    document.myform.submit()
}

function do_off()
{
    house_code = document.myform.house_code.value
    if (house_code == "")
    {
        house_code = '6C6C6'
    }
    device_index = document.myform.device_index.value

    document.myform.action = '/legacy_learn/off/' + house_code + '/' + device_index
    document.myform.submit()
}
</script>

%try:
   Device is: {{state}}<BR>
%  house_code = hex(house_code)[2:]
%except:
%   house_code=""
%   device_index=""
%end

<form method='get' name='myform'>
House code: <input type='text' id='house_code' value='{{house_code}}'><BR>
device index: <input type='text' id='device_index' value='{{device_index}}'><BR>

<button type='button' onclick='do_on()'>ON</a>
<button type='button' onclick='do_off()'>OFF</a>
</form>
