function showAnswer(ans)
{
	var q = document.getElementsByClassName("question")
	console.log(q)
	chosen=document.querySelector('input[name="answer"]:checked').value;
	console.log(ans, Number(chosen)) //3 ,2 
	if(ans==Number(chosen))
	{
		var res = document.getElementsByClassName("result")[0]
		res.text("correct")
	}
	else
	{
		res.text("Wrong")
	}
	q[0].style.display="none"
	 document.getElementsByClassName("answer")[0].style.display = "block"
	 	 $.ajax({url: "/learn/know", 
	 	 	 type: "POST",
	 	success: function(result){
	 		console.log("insuccess")
    }}
    );
}





function backToQuestion()
{
	var q = document.getElementsByClassName("question")
	console.log(q)
	q[0].style.display="block"
	 document.getElementsByClassName("answer")[0].style.display = "none"

}