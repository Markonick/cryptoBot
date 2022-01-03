import GetSymbolId from './GetSymbolId'

function Logo(props) {
  const id = GetSymbolId(props.symbol);
  const url = `https://s2.coinmarketcap.com/static/img/coins/32x32/${id}.png`;
  
  return (
    <div>  
        <img 
            src={url}
            style={{height: "30px", position: "relative",}}
            className="Symbol-logo"
            alt={props.symbol}
        />
    </div>
  );
}

export default Logo;
