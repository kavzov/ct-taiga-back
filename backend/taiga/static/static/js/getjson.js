var data;
$.ajax({
  type: 'GET',
  url: "http://localhost:8000/users/5/",
  data: data,
  async: true,
  contentType: 'application/json;indent=4;charset=utf-8',
  beforeSend: function (xhr) {
    if (xhr && xhr.overrideMimeType) {
      xhr.overrideMimeType('application/json;indent=4;charset=utf-8');
    }
  },
  dataType: 'json',
  success: function (data) {
    $('#test').text(JSON.stringify(data));
    console.log(data);
//    alert(data.username);
  }
});
