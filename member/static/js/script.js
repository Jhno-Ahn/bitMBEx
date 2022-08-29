 
var idcheck = "아이디를 입력하세요"; 
var passwdck = "비밀번호를 입력하세요";
var repasswdck = "비밀번호가 다릅니다";
var nameck = "이름을 입력하세요";


// 중복확인
function confirm() {
	if( ! inputform.id.value ) {
		alert( idcheck );
		inputform.id.focus()
	} else {
		url = "confirm" + "?id=" + inputform.id.value 
		open( url, "cofirm", "toolbar=no, menubar=no, scrollbar=no, status=no, width=500, height=300" )
	}
}
function setid( id ) {
	opener.document.inputform.id.value = id;
	window.close();
}

// 가입 페이지
function inputcheck() {
	if( ! inputform.id.value ) {
		alert( idcheck );
		inputform.id.focus();
		return false;
	} else if( ! inputform.passwd.value ) {
		alert( passwdck );
		inputform.passwd.focus();
		return false;
	} else if( inputform.passwd.value != inputform.repasswd.value ) {
		alert( repasswdck );
		inputform.passwd.focus();
		return false;
	} else if( ! inputform.name.value ) {
		alert( nameck );
		inputform.name.focus();
		return false;
	}	
}

// 메인 페이지
function maincheck() {
	if( ! mainform.id.value ) {
		alert( idcheck );
		mainform.id.focus();
		return false;		
	} else if( ! mainform.passwd.value ) {
		alert( passwdck );
		mainform.passwd.focus();
		return false;
	}
}







