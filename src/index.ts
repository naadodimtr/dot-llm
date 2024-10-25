import * as fs from "fs";

// So we need to create dataset of Alphanumeric characters a-zA-Z0-9 and Special Characters like !"#$%&'()*+,-/:;<=>?@[\]^_`{|}~.
const appendToFile = __dirname + "/../data/input.txt";

// For every character in the above set, append a . character to it to form the first line,
// so we need ASCII chars from 32-126 including 32 and 126
const asciiArray = Array.from({length: 95}, (_, index) => index + 32);
const asciiString = String.fromCharCode(...asciiArray)

// console.log(asciiString)
// the above will print `` !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~``
// there is a space character in front of !
// console.log(Array.from(asciiString))

let asciiStringArray: string[] = Array.from(asciiString)
for(let i=0; i < asciiString.length; i++){
    // this will append a . char to every other character in the array
    const rowString = asciiStringArray.map(char => char + ".").join("")
    // console.log(asciiStringArray)
    // console.log(rowString + "\n")
    fs.appendFileSync(appendToFile, rowString + "\n");

    // Shift the first element to the last
    const firstElement = String(asciiStringArray.shift())
    asciiStringArray.push(firstElement)
}

// now we have shifted possible combinations of data

console.log('Done')