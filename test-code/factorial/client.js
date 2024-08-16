const axios = require('axios');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const url = 'http://127.0.0.1:5000/factorial'

rl.question('Enter a number : ', async (input) => {

    const number = parseInt(input, 10);

    if (isNaN(number)) {
        console.error('Invalid number');
        rl.close();
        return;
    }

    try {
        const response = await axios.post(url,
            {
                number: number
            });

        if (response.data.factorial !== undefined) {
            console.log('Factorial:', response.data.factorial);
        } else if (response.data.error !== undefined) {
            console.error(response.data.error);
        }
    } catch (error) {
        console.error('Error:', error.response ? error.response.data.error : error.message);
    } finally {
        rl.close();
    }
});
