function statusChangeCallback(response) {
  console.log('statusChangeCallback');
  console.log(response);

  if (response.status === 'connected') {
    sendToServer(response);
  } else if (response.status === 'not_authorized') {
    // The person is logged into Facebook, but not your app.
    // document.getElementById('status').innerHTML = "<fb:login-button scope='public_profile,email' onlogin='checkLoginState();'>;
    //   </fb:login-button>";
  } else {
    // The person is not logged into Facebook, so we're not sure if
    // they are logged into this app or not.
    // document.getElementById('status').innerHTML = "<fb:login-button scope='public_profile,email' onlogin='checkLoginState();'>;
    //   </fb:login-button>";
  }
}

function sendToServer(response) {
  var url = "/console/fb_login/";
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
      document.location.reload(false);
      resp = xmlHttp.responseText;
      var temp = resp.split(",")

      var redirurl = "https://pitangui.amazon.com/spa/skill/account-linking-status.html?vendorId=M2ZAY1TEQE0B7D#state="
                    + temp[0] + "&access_token=" + temp[1] + "&token_type=Bearer"

      top.location.href =  redirurl
    } else if (xmlHttp.status == 401) {
        console.log('login failed');
        // document.getElementById("error_msg").style.visibility = "visible";
        $('#error_msg').show();
    }
  }
  xmlHttp.open( "GET", url, true); // false for synchronous request
  xmlHttp.setRequestHeader("ACCESS", response.authResponse.accessToken);
  // console.log(response.authResponse.accessToken);
  xmlHttp.setRequestHeader("UserID", response.authResponse.userID);
  xmlHttp.send();
}

window.fbAsyncInit = function() {
    FB.init({
      appId      : '1592333431017055',
      cookie     : true,
      xfbml      : true,
      version    : 'v2.8'
    });
    FB.AppEvents.logPageView();
  };
  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));

   function checkLoginState() {
     FB.getLoginStatus(function(response) {
       statusChangeCallback(response);
     });
   }
