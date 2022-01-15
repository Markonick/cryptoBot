import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableFooter from '@mui/material/TableFooter';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import IconButton from '@mui/material/IconButton';
import FirstPageIcon from '@mui/icons-material/FirstPage';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import LastPageIcon from '@mui/icons-material/LastPage';
import { IOrder, ISignal, IBinanceOrderResponse } from '../../customTypes';

interface TablePaginationActionsProps {
  count: number;
  page: number;
  rowsPerPage: number;
  onPageChange: (
    event: React.MouseEvent<HTMLButtonElement>,
    newPage: number,
  ) => void;
}

function TablePaginationActions(props: TablePaginationActionsProps) {
  const theme = useTheme();
  const { count, page, rowsPerPage, onPageChange } = props;

  const handleFirstPageButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>,
  ) => {
    onPageChange(event, 0);
  };

  const handleBackButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onPageChange(event, page - 1);
  };

  const handleNextButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onPageChange(event, page + 1);
  };

  const handleLastPageButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onPageChange(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1));
  };

  return (
    <Box sx={{ flexShrink: 0, ml: 2.5 }}>
      <IconButton
        onClick={handleFirstPageButtonClick}
        disabled={page === 0}
        aria-label="first page"
      >
        {theme.direction === 'rtl' ? <LastPageIcon /> : <FirstPageIcon />}
      </IconButton>
      <IconButton
        onClick={handleBackButtonClick}
        disabled={page === 0}
        aria-label="previous page"
      >
        {theme.direction === 'rtl' ? <KeyboardArrowRight /> : <KeyboardArrowLeft />}
      </IconButton>
      <IconButton
        onClick={handleNextButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="next page"
      >
        {theme.direction === 'rtl' ? <KeyboardArrowLeft /> : <KeyboardArrowRight />}
      </IconButton>
      <IconButton
        onClick={handleLastPageButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="last page"
      >
        {theme.direction === 'rtl' ? <FirstPageIcon /> : <LastPageIcon />}
      </IconButton>
    </Box>
  );
}

function createRow(
  symbolId: number,
  orderID: number,
  value: string,
  rsi: number,
  previRsi: number,
  createdAt: number,
  clientOrderId: number,
  transactTime: number,
  price: number,
  origQty: number,
  executedQty: number,
  cummulativeQuoteQty: number,
  status: string,
  timeInForce: string,
  type: string,
  side: string,
) {
    return { 
      symbolId, 
      orderID, 
      value, 
      rsi, 
      previRsi, 
      createdAt,
      clientOrderId,
      transactTime,
      price,
      origQty,
      executedQty,
      cummulativeQuoteQty,
      status,
      timeInForce,
      type,
      side, 
    };
  }

interface TableProps {
  orders: IOrder[];
}

export const OrdersTable: React.FC<TableProps> = (props:TableProps) => {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);
  const {orders} = props;
  const rows = orders.map((order) => {
    return createRow(
      order.signalDetails.symbol_id, 
      order.signalDetails.order_id, 
      order.signalDetails.value, 
      order.signalDetails.curr_rsi, 
      order.signalDetails.prev_rsi, 
      order.signalDetails.created_at,
      order.orderResponse.clientOrder_id,
      order.orderResponse.transactTime,
      order.orderResponse.price,
      order.orderResponse.origQty,
      order.orderResponse.executedQty,
      order.orderResponse.cummulativeQuoteQty,
      order.orderResponse.status,
      order.orderResponse.timeInForce,
      order.orderResponse.type,
      order.orderResponse.side, );
  });
  // Avoid a layout jump when reaching the last page with empty rows.
  const emptyRows =
    page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0;

  const handleChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number,
  ) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  
  console.log(orders)
  return (
    <TableContainer component={Paper} style={{margin: 80}}>
      <Table sx={{ minWidth: 500 }} aria-label="custom pagination table">
        <TableBody>
          {(rowsPerPage > 0
            ? orders.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
            : orders
          ).map((row) => (
            <TableRow key={row.orderResponse.clientOrder_id}>
              <TableCell component="th" scope="row">
                {row.orderResponse.clientOrder_id}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.signalDetails.value}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.signalDetails.curr_rsi}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.signalDetails.curr_rsi}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.signalDetails.order_id}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.signalDetails.created_at}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.orderResponse.price}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.orderResponse.cummulativeQuoteQty}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.orderResponse.executedQty}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.orderResponse.origQty}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.orderResponse.side}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.orderResponse.status}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.orderResponse.timeInForce}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.orderResponse.transactTime}
              </TableCell>
              <TableCell style={{ width: 100, color: "white", fontSize: 8, }} align="right">
                {row.orderResponse.type}
              </TableCell>
            </TableRow>
          ))}
          {emptyRows > 0 && (
            <TableRow style={{ height: 53 * emptyRows }}>
              <TableCell colSpan={6} />
            </TableRow>
          )}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TablePagination
              rowsPerPageOptions={[5, 10, 25, { label: 'All', value: -1 }]}
              colSpan={3}
              count={rows.length}
              rowsPerPage={rowsPerPage}
              page={page}
              SelectProps={{
                inputProps: {
                  'aria-label': 'rows per page',
                },
                native: true,
              }}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
              ActionsComponent={TablePaginationActions}
            />
          </TableRow>
        </TableFooter>
      </Table>
    </TableContainer>
  );
}
