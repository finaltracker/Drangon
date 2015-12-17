function calculator() {
  var a = document.getElementById("num_one").value;
  var b = document.getElementById("num_two").value;
  var res = androidInterfaceMethod.calculator(a, b);
  document.getElementById("result").innerHTML = res;
}
