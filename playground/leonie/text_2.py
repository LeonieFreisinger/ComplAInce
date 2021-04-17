import os
import regex
import mdutils

const regexMdLinks = /\[([^\[]+)\](\(.*\))/gm

// Example md file contents
const mdContents = `
Lorem ipsum dolor sit amet, consectetur adipiscing elit..

[hello link](/admin/table_edit/table_edit.cfm?action=edit&table_name=organizationsXcategories)

Lorem ipsum dolor sit amet, consectetur adipiscing elit..

[otherLink](https://google.com)

Lorem ipsum dolor sit amet, consectetur adipiscing elit..

[third link](https://google.com)
`

const matches = mdContents.match(regexMdLinks)
console.log('links', matches)

const singleMatch = /\[([^\[]+)\]\((.*)\)/
for (var i = 0; i < matches.length; i++) {
  var text = singleMatch.exec(matches[i])
  console.log(`Match #${i}:`, text)
  console.log(`Word  #${i}: ${text[1]}`)
  console.log(`Link  #${i}: ${text[2]}`)
}