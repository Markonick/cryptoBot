import data from './coinmarketcapMap'
 
function GetSymbolId(symbol) {
  return data.filter(item => item.symbol === symbol.toUpperCase()).map(item => item.id)
}

export default GetSymbolId;