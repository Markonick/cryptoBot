import React from 'react';
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { makeStyles } from '@mui/styles';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import SymbolLogo from "./SymbolLogo";
import Ticker from "./Ticker";
import TimeSeries from './TimeSeries';
import { PostPush } from '../../api/PostPush';
// import GetKlineData from './api/GetKlineData';


// const symbols = [
  // "btc", "xrp", "doge", "xlm", "trx", "eos", "ltc", "miota", "xmr", "link",
  // "etn", "rdd", "strax", "npxs", "glm", "aave", "sol", "atom", "cro", "ht",
  // "mkr", "snx", "algo", "ksm", "comp", "vgx", "ftm", "zec", "rune", "cel",
  // "rev", "icx", "hbar", "chsb", "iost", "zks", "lrc", "omg", "pax", "husd",
  // "vet", "sc", "btt", "dash", "xtz", "bch", "bnb", "ada", "usdt", "dcn",
  // "tfuel", "xvg", "rvn", "bat", "dot", "theta", "luna", "neo", "ftt", "dai",
  // "egld", "fil", "leo", "sushi", "dcr", "ren", "nexo", "zrx", "okb", "waves",
  // "dgb", "ont", "bnt", "nano", "matic", "xwc", "zen", "btmx", "qtum", "hnt",
  // "kndc", "delta", "pib", "opt", "acdc", "eth",
// ];
const symbols = [
  "btc", "xrp" ];
const currency = 'usdt';
const MIN_WIDTH = 40;
const columns = [
  {
    id: 'logo',
    label: '',
    minWidth: MIN_WIDTH, },
  {
    id: 'symbol',
    label: 'Symbol',
    minWidth: MIN_WIDTH,
    align: 'right',
    format: (value) => value.toLocaleString('en-US'),
  },
  {
    id: 'price',
    label: 'Price',
    minWidth: MIN_WIDTH,
    align: 'right',
    format: (value) => value.toLocaleString('en-US'),
  },
  {
    id: 'change',
    label: 'Change +/-',
    minWidth: MIN_WIDTH,
    align: 'right',
    format: (value) => value.toFixed(2),
  },
  {
    id: 'mini-series',
    label: '24h',
    minWidth: MIN_WIDTH,
    align: 'right',
    format: (value) => value.toLocaleString('en-US'),
  },
];

const theme = createTheme({
    overrides: {
        MuiCssBaseline: {
            '@global': {
                '*': {
                    'scrollbar-width': 'thin',
                },
                '*::-webkit-scrollbar': {
                    width: '2px',
                    height: '2px',
                    background: "#555",
                }
            }
        }
    }
});

const useStyles = makeStyles({
  root: {
    backgroundColor: "#1c1c1f",
    color: "white",
    width: "auto",
    margin: 40,
    borderRadius: "12px",
    padding: 10,
  },
  container: {
    // background: "red",
    minHeight: 'inherit',
    maxHeight: 'inherit',
    color: "white",
    // backgroundColor: "#1c1c1f",
    // backgroundColor: "red",
  },
  row: {
    color: "white",
    fontSize: 10,
    fontStyle: "normal",
    fontWeight: "100",
    fontFamily: 'normal 100%/1.5 "Dosis", sans-serif',
    WebkitFontSmoothing: 'antialiased',
  }
});

const createRow = (logo, symbol, price, change, miniseries) => {
  return { logo, symbol, price, change, miniseries };
}

const rows = symbols.map((symbol) => {
  const logo = <SymbolLogo symbol={symbol} />;
  let tick = <Ticker symbol={symbol} currency={currency} />;
  // let miniseries = <TimeSeries symbol={symbol} currency={currency} />;
  console.log(tick)
  return createRow(logo, symbol.toUpperCase(), tick, "", "miniseries");
});

const rowsDict = Object.assign({}, ...rows.map((x) => ({ [x.symbol]: x })));
console.log(rowsDict['XRP'])
export default function CryptosTable() {
  const classes = useStyles();
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(1);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(event.target.value);
    setPage(0);
  };


  const data = PostPush(symbols);
  console.log(rows)
  return (
    <Paper className={classes.root} >
      <ThemeProvider theme={theme}>
        <TableContainer className={classes.container} >
          <Table stickyHeader size="small" aria-label="sticky table">
            <TableHead >
              <TableRow >
                {columns.map((column) => (
                  <TableCell 
                    key={column.id}
                    align={column.align}
                    style={{
                      maxWidth: column.minWidth,
                      minWidth: column.minWidth,
                      backgroundColor: "inherit",
                      color: "white"
                    }}
                  >
                    {column.label}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row) => {
                return (
                  <TableRow hover role="checkbox" tabIndex={-1} key={row.code}>
                    {columns.map((column) => {
                      const value = row[column.id];
                      return (
                        <TableCell className={classes.row} key={column.id} align={column.align} style={{
                          color: "white",
                          backgroundColor: "inherit",
                        }}>
                          {column.format && typeof value === 'number' ? column.format(value) : value}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </ThemeProvider>
      <TablePagination
        rowsPerPageOptions={[10, 25, 100]}
        component="div"
        count={rows.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onChangePage={handleChangePage}
        onChangeRowsPerPage={handleChangeRowsPerPage}
      />
      </Paper>
  );
}
