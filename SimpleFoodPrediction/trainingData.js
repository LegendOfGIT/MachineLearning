const food_beer = { beer: 1 };
const food_burger = { burger: 1 };
const food_burger_coffee = { burger: 1, coffee: 1 };
const food_burger_fries = { burger: 1, fries: 1 };
const food_burger_fries_coke = { burger: 1, fries: 1, coke: 1 };
const food_burger_beer = { burger: 1, beer: 1 };
const food_burger_fries_beer = { burger: 1, fries: 1, beer: 1 };;
const food_buns_coffee = { buns: 1, coffee: 1 };
const food_coffee = { coffee: 1 };
const food_coffee_cake = { coffee: 1, cake: 1 };

const food_propabilities = [
	{
		timeOfDayFrom: 0,	//	00:00	
		timeOfDayTo: 3600,	//	01:00
		averageNumberOfGuestsPerMinute: 15,
		propabilities: [
			{ percentage: 75, food: food_coffee },
			{ percentage: 15, food: food_burger_fries },
			{ percentage: 10, food: food_burger_beer },
		]
	},
	{
		timeOfDayFrom: 3601,	//	01:00	
		timeOfDayTo: 10800,		//	03:00
		averageNumberOfGuestsPerMinute: 5,
		propabilities: [
			{ percentage: 60, food: food_coffee },
			{ percentage: 10, food: food_burger },
			{ percentage: 15, food: food_burger_beer },
			{ percentage: 15, food: food_beer },
		]
	},
	{
		timeOfDayFrom: 10801,	//	03:00	
		timeOfDayTo: 21600,		//	06:00
		averageNumberOfGuestsPerMinute: 12,
		propabilities: [
			{ percentage: 40, food: food_coffee },
			{ percentage: 40, food: food_buns_coffee },
			{ percentage: 10, food: food_burger },
			{ percentage: 10, food: food_burger_coffee },
		]
	},
];

function generateTraingData(timespanInSeconds){
	trainingData = [];

	for(second=0;second<timespanInSeconds;second+=60){
		const timeOfDay = second % 86400;
		
		let numberOfGuests = 0;
		const propabilities = food_propabilities.map(food_propability => {
			numberOfGuests = food_propability.averageNumberOfGuestsPerMinute;
			
			if (food_propability.timeOfDayFrom <= timeOfDay && timeOfDay <= food_propability.timeOfDayTo) {
				return food_propability.propabilities.map(propability => {				
					return propability;
				});
			}
		});
		
		for(i=0;i<propabilities.length;i++){
			if(undefined !== propabilities[i]){
				let foodItemsForRandomChoice = [];
				propabilities[i].map(propability => {
					for(i=0;i<propability.percentage;i++){
						foodItemsForRandomChoice.push(propability.food);
					}
				})
				
				for(i=0;i<numberOfGuests;i++){
					trainingData.push({ input: { timeOfDay: timeOfDay / 100000 }, output: foodItemsForRandomChoice[Math.floor(Math.random() * 100)] });
				}
			}
		}
	}
			
	return trainingData;
}