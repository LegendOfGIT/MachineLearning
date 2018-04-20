const filler = 0.00;

const startpage = 0.10;
const overview = 0.20;
const overview_next_page = 0.30;
const overview_prev_page = 0.40;
const spv = 0.50;
const add_to_basket = 0.60;
const checkout = 0.70;
const activity_timeout = 0.90;

const trainingData = [
	{ input: [startpage , overview , overview_next_page , overview_next_page , spv , add_to_basket], output: { checkout: 1 } },
	{ input: [startpage , filler , filler , filler , filler , filler], output: { overview: 1 } },
	{ input: [startpage , overview , filler , filler , filler , filler], output: { overview_next_page: 1 } },

	{ input: [startpage , filler , filler , filler , filler , filler], output: { checkout: 1 } },

	{ input: [startpage , overview , overview_next_page , spv , add_to_basket , filler], output: { checkout: 1 } },
	{ input: [startpage , filler , filler , filler , filler , filler], output: { overview: 1 } },
	{ input: [startpage , overview , filler , filler , filler , filler], output: { overview_next_page: 1 } },

	{ input: [overview_next_page , spv , add_to_basket , filler , filler , filler], output: { activity_timeout: 1 } },
	{ input: [overview_next_page , filler , filler , filler , filler , filler], output: { spv: 1 } },
	{ input: [overview_next_page , spv , filler , filler , filler , filler], output: { add_to_basket: 1 } },

	{ input: [startpage , filler , filler , filler , filler , filler], output: { checkout: 1 } },	
	
	{ input: [startpage , overview , overview_next_page , overview_next_page , overview_next_page , overview_next_page], output: { activity_timeout: 1 } },
	{ input: [startpage , filler , filler , filler , filler , filler], output: { overview: 1 } },
	{ input: [startpage , overview , filler , filler , filler , filler], output: { overview_next_page: 1 } },
	
	{ input: [startpage , overview , overview_next_page , overview_next_page , overview_next_page , filler], output: { activity_timeout: 1 } },
	{ input: [startpage , filler , filler , filler , filler , filler], output: { overview: 1 } },
	{ input: [startpage , overview , filler , filler , filler , filler], output: { overview_next_page: 1 } },

	{ input: [startpage , overview , overview_next_page , filler , filler , filler], output: { activity_timeout: 1 } },
	{ input: [startpage , filler , filler , filler , filler , filler], output: { overview: 1 } },
	{ input: [startpage , overview , filler , filler , filler , filler], output: { overview_next_page: 1 } },

	{ input: [startpage , filler , filler , filler , filler , filler], output: { checkout: 1 } },

	{ input: [startpage , filler , filler , filler , filler , filler], output: { checkout: 1 } },

	{ input: [overview , overview_next_page , spv , add_to_basket , filler , filler], output: { checkout: 1 } },
	{ input: [overview , filler , filler , filler , filler , filler], output: { overview_next_page: 1 } },
	{ input: [overview , overview_next_page , filler , filler , filler , filler], output: { spv: 1 } },

	{ input: [startpage , filler , filler , filler , filler , filler], output: { checkout: 1 } },

	{ input: [startpage , overview , overview_next_page , overview_next_page , spv , add_to_basket], output: { checkout: 1 } },
	{ input: [startpage , filler , filler , filler , filler , filler], output: { overview: 1 } },
	{ input: [startpage , overview , filler , filler , filler , filler], output: { overview_next_page: 1 } },

	{ input: [startpage , overview , overview_next_page , overview_next_page , filler , filler], output: { activity_timeout: 1 } },
	{ input: [startpage , filler , filler , filler , filler , filler], output: { overview: 1 } },
	{ input: [startpage , overview , filler , filler , filler , filler], output: { overview_next_page: 1 } },

	{ input: [startpage , filler , filler , filler , filler , filler], output: { checkout: 1 } },
	{ input: [startpage , filler , filler , filler , filler , filler], output: { checkout: 1 } }
];