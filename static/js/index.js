$(document).ready(function() {
	console.log("Hello again!");
	
	function sendQuery() {
		let query = ""
		$.ajax(
			{
				url: "local_test_query?query=how+many+neutrons+in+an+argon+molecule"+query,
				
				success: function(result){
					//console.log(result)
					
					for (const [key, value] of Object.entries(result)) {
						if (value[0][0] == "B") {
							$("#bingCol").append(`
								<div class="card" style="width: 18rem;">
									<div class="card-body">
										<h5 class="card-title">${value[0]}</h5>
										<h6 class="card-subtitle mb-2 text-muted"><a href='${key}'>Link</a></h6>
										<p class="card-text">Keyword hits = ${value[2]}</p>
									</div>
								</div>
							`)
						} else {
							$("#googleCol").append(`
								<div class="card" style="width: 18rem;">
									<div class="card-body">
										<h5 class="card-title">${value[0]}</h5>
										<h6 class="card-subtitle mb-2 text-muted"><a href='${key}'>Link</a></h6>
										<p class="card-text">Keyword hits = ${value[2]}</p>
									</div>
								</div>
							`)
						}
					}
				}
			}
		);
	}
	sendQuery();
	
})