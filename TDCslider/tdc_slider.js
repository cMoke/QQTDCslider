function LongNumtoCode(longNum){
    var offsets = [0,8,16,24];
    var codes = [];
    for (var a of offsets){
        codes.push(longNum>>a&255);
    }
    return String.fromCharCode.apply(String,codes);
};


function strToLongNum(str){
    
    var offsets = [0,8,16,24];
    var longNum = 0;
    for(let i = 0;i<str.length;i++){
        longNum = longNum| (str.charCodeAt(i)<<offsets[i])
    }
    return longNum;
};

function teaEncryptBlock(num_lis, key){
    var num1 = num_lis[0];
    var num2 = num_lis[1];
    var sum = 0;
    key = [1347898179, 1263881580, 1246389057, 1382638164];
    var delta = 2654435769;
    for (var i = 0; i < 32; i++) {
        num1 += (((num2 << 4) ^ (num2 >>> 5)) + num2) ^ (sum + key[sum & 3]);
        sum += delta;
        num2 += (((num1 << 4) ^ (num1 >>> 5)) + num1) ^ (sum + key[(sum >> 11) & 3]);
    }
    return [num1, num2];
}

function teaDecryptBlock(num_ls,key){
    let num1 = num_ls[0];
    let num2 = num_ls[1];
    let delta = 2654435769;
    let sum = delta*32;
    
    key = [1347898179, 1263881580, 1246389057, 1382638164];
    
    for (var i=0; i<32; i++) {
    
       num2_sub = (num1<<4)^(num1>>>5)
       num2_sub+= num1
       num2-= num2_sub^(sum + key[(sum >> 11) & 3]);
       sum -= delta;
       num1 -= (((num2 << 4) ^ (num2 >>> 5)) + num2) ^ (sum + key[sum & 3]);
        // console.log("num1", num1,'key',key[sum & 3]);
    }
    return [num1, num2];
}
function LongNumTostr(longnum){
    var a =new Array(longnum.length);
    for(var i = 0;i<longnum.length;i++){
        a[i] = String.fromCharCode(longnum[i] & 0xFF, longnum[i] >>> 8 & 0xFF,
            longnum[i] >>> 16 & 0xFF, longnum[i] >>> 24 & 0xFF);
    }
    return a.join('');
}
function CodetoLongNum(codes){
    var longNum = 0;
    var offsets = [0,8,16,24];
    for (var i = 0;i<codes.length;i++){
        longNum +=codes[i]<<offsets[i]>>>0;
    }
    return longNum;
}

function getOriginCode(encode){
    code = window.atob(encode);
    debugger;
    length = code.length;
    var LongNumList = [];
    for(var i = 0;i<length/4;i++){
        var sinceCode = [];
        for(var j = 0;j<4;j++){
            sinceCode.push(code.charCodeAt(i*4+j));
        }
        LongNumList.push(CodetoLongNum(sinceCode))
    }
    decodetext = '';
    LongNumList2 = [];
    for(var i = 0;i<length/4;i+=2){
        LongNumList2.push(teaDecryptBlock([LongNumList[i],LongNumList[i+1]]));
    }
    for(var i = 0;i<LongNumList2.length;i+=1){
        decodetext+=LongNumTostr([LongNumList2[i][0]])+LongNumTostr([LongNumList2[i][1]]);
    }
    return decodetext;
}
const _keyStr =
  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
function btoa(input) {
  let output = "";
  let chr1, chr2, chr3, enc1, enc2, enc3, enc4;
  let i = 0;

  while (i < input.length) {
    chr1 = input.charCodeAt(i++);
    chr2 = input.charCodeAt(i++);
    chr3 = input.charCodeAt(i++);

    enc1 = chr1 >> 2;
    enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
    enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
    enc4 = chr3 & 63;

    if (isNaN(chr2)) {
      enc3 = enc4 = 64;
    } else if (isNaN(chr3)) {
      enc4 = 64;
    }

    output =
      output +
      _keyStr.charAt(enc1) +
      _keyStr.charAt(enc2) +
      _keyStr.charAt(enc3) +
      _keyStr.charAt(enc4);
  }
  return output;
};

function encodeTDCslider(text){
    var encodeText = '';
    //debugger;
    var length = text.length;
    var LongNumList1 = [];
    var LongNumList2 = [];
    for(var i = 0; i< length;i+=4){
        LongNumList1.push(strToLongNum(text.substring(i,i+4)));
    }  
   
    for(var i = 0;i<length/4;i+=2){
        if(LongNumList1[i]==125) {LongNumList2.push([2848324329,1938020559]); continue;}
        LongNumList2.push(teaEncryptBlock([LongNumList1[i],LongNumList1[i+1]]));
    }
   
    for(var i = 0;i<LongNumList2.length;i+=1){
       encodeText+=LongNumtoCode([LongNumList2[i][0]])+LongNumtoCode([LongNumList2[i][1]]);
    }
    
    encodeText = btoa(encodeText);
    return encodeText;
};