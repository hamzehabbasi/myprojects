


add_cash = () => {
this.request.request = 'add_cash';
if (this.request.amount === 0) {
return this.doNext({
result: 'failed',
message: TEXT.NOT_AMOUNT,
});
}
virdaar_apply_cmd(this.request).then(r => {
switch (r.status) {
case 402:
return this.doNext({result: 'gateway', gateway: r.data.link});
case 462:
return this.doNext({
result: 'failed',
message: XTEXT.ONLINE_PAYMENT_NOT_POSSIBLE,
cmd: 'renew_subscription',
});
case 419:
return this.doNext({
result: 'failed',
message: TEXT.LIMITED_ACCOUNT,
});
case 425:
return this.doNext({
result: 'failed',
message: TEXT.NO_INTERNET,
});
default:
return this.doNext({
result: 'failed',
message: TEXT.SERVER_CRASHED_ERROR,
});
}
});
};