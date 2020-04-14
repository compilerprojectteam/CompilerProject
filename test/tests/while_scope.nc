int var;

void func(void) {
	var = 1;
}

void outfunc(void) {
	output(var);
}

void func1(int var) {
	int a;
	int b;
	void func(void) {
		var = 2;
	}
	int c;
	int d;
	a = 20;
	b = 200;
	c = 2000;
	d = 200;
	while (var < 2) {
		int var;
		var = 1;
		output(var);
		func();
	}
	while (a < d) {
		int func(void) {
			if (b < c) {
				int a;
				a = 10;
				b = b + 1000;
				return a;
			} else {
				a = a + 20;
				output(a);
				return 20;
			}
			return 0;
		}
		d = d - func();
		output(a);
		output(d);
	}
}

void main(void) {
	int var;
	func();
	var = 10;
	outfunc();
	func1(0);
	output(var);
	outfunc();
	if (var == 1) {
		int var;
		var = 1000;
		output(var);
	} else {
		int var;
		var = 100;
	}
	output(var);
}
	