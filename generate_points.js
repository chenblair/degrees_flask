const username = "test1";

// not counting first point
const iterations = 25;


const send = async (username, iterations) => {
	// generate first points (starting at MIT media lab)
	let lat = 42.3610451;
	let lng = -71.0958224;

	let delta = (Math.random() / 5000) - 0.0001;
	delta /= 1.5;
	lat += delta;

	delta = (Math.random() / 5000) - 0.0001;
	delta /= 1.5;
	lng += delta;

	for (let i = 0; i < iterations; i++) {
		// send to server
		let res = await fetch(`https://hackmit-degrees.herokuapp.com/add_new_location`, {
			method: "POST",
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({username, lat, lng})
		})
		console.log(`Iteration ${i}: `, await res.json())

		// generate new random (staying within +-0.000005)
		delta = (Math.random() / 5000) - 0.0001;
		delta /= 2;
		lat += delta;

		delta = (Math.random() / 5000) - 0.0001;
		delta /= 2;
		lng += delta;
	}
}

send(username, iterations)
	.then(res => { console.log('completed!') })
