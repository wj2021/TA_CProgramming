#include<iostream>
#include<conio.h>
#include<cstdlib>

using namespace std;

/**
 * 控制台显示从公元1年1月到以后的日历
 */
// 现行格里高利历非闰年每月天数，下标从1开始
const static int daysOfMonths[13] = { 0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };
const static char weekNames[7][4] = { { 'S', 'u', 'n' }, { 'M', 'o', 'n' }, { 'T', 'u', 'e' },
		                              { 'W', 'e', 'd' }, { 'T', 'u', 'r' },
		                              { 'F', 'r', 'i' }, { 'S', 'a', 't' } };
struct Calendar {
	int year;
	int month;
	int day;
	int week;

	Calendar(int yy, int mm, int dd) {
		year = yy;
		month = mm;
		day = dd;
		week = 0;
	}

	/*
	 * 1582年之前采用儒略历，采用四年一闰
	 * 1582年以后的格里高利历采用4年一闰，百年不闰，400年一闰的规定来弥补儒略历的缺陷
	 */
	bool isLeapYear() {
		if (this->year < 1582) {
			if (this->year % 4 == 0) {
				return true;
			}
		} else {
			if ((this->year % 4 == 0 && this->year % 100 != 0)
					|| this->year % 400 == 0)
				return true;
		}
		return false;
	}

	//根据公元元年1月1日的星期来计算当前日期的星期
	int getWeekNum() {
		Calendar first(1, 1, 1);
		first.week = 6; // 按照现行的公历公元1年1月1日为星期六
		while (first < this) {
			first.addDay();
		}
		return first.week;
	}

	// 将日期向后加1天
	void addDay() {
		if (this->year == 1582 && this->month == 10 && this->day == 4) {
			// 由于历法误差，1582-10-5到1582-10-14号在日历上不存在（从儒略历改为格里高利历）
			this->day = this->day + 11;
			this->week = (this->week + 1) % 7;
		} else {
			int daysOfMonth = daysOfMonths[this->month];
			if (this->isLeapYear() && this->month == 2)
				daysOfMonth = 29;
			this->day = this->day + 1;
			this->week = (this->week + 1) % 7;
			if (this->day > daysOfMonth) {
				this->day = 1;
				addMonth();
			}
		}
	}

	// 将月份加1
	void addMonth() {
		this->month = this->month + 1;
		if (this->month > 12) {
			this->month = 1;
			this->year = this->year + 1;
		}
	}

	// 将月份减1
	void decMonth() {
		this->month = this->month - 1;
		if (this->month < 1) {
			this->month = 12;
			this->year = this->year - 1;
			if (this->year < 1) {
				this->year = 1;
				this->month = 1;
			}
		}
	}

	// 重载比较2个日期大小的运算符
	bool operator<(const Calendar *c) {
		if (this->year < c->year) {
			return true;
		} else if (this->year == c->year) {
			if (this->month < c->month) {
				return true;
			} else if (this->month == c->month) {
				if (this->day < c->day) {
					return true;
				}
			}
		}
		return false;
	}

	// 打印显示当前月份的日历
	void print() {
		cout << endl << "\t" << "\t" << "    " << year << "-" << month << endl;
		for (int k = 0; k < 7; ++k)
			cout << weekNames[k] << "\t";
		cout << endl;
		int week = this->getWeekNum();
		int restSpace = 7;
		for (int i = 0; i < week; ++i) {
			cout << "\t";
			restSpace--;
		}
		int days = daysOfMonths[this->month];
		if (this->isLeapYear() && this->month == 2)
			days = 29;
		if (this->year == 1582 && this->month == 10)
			days = 21; // 该月被人为地扣除了10天
		for (int j = 0; j < days; ++j) {
			if (restSpace > 0) {
				int day = 0;
				if (this->year == 1582 && this->month == 10 && j > 3)
					day = j + 11;
				else
					day = j + 1;
				if (day < 10)
					cout << " ";
				cout << day << "\t";
				restSpace--;
			} else {
				cout << endl;
				j--;
				restSpace = 7;
			}
		}
		cout << endl << endl;
		cout << "W: Last Month" << "\t" << "S: Next Month" << "\t"
				<< "A: Last Year" << "\t" << "D: Next Year" << endl;
	}
};

int main() {
	int year, month;
	do {
		cout << "Please input the current year and month split with space: ";
		cin >> year >> month;
	} while (!(year > 0 && month > 0 && month < 13));
	Calendar calendar(year, month, 1);
	calendar.print();

	char ch;
	while (true) {
		ch = _getch();
		switch (ch) {
		case 'W':
		case 'w': // 上个月
			system("cls");
			calendar.decMonth();
			calendar.print();
			break;
		case 'S':
		case 's': // 下个月
			system("cls");
			calendar.addMonth();
			calendar.print();
			break;
		case 'A':
		case 'a': // 上一年
			system("cls");
			calendar.year--;
			if (calendar.year < 1)
				calendar.year = 1;
			calendar.print();
			break;
		case 'D': // 下一年
		case 'd':
			system("cls");
			calendar.year++;
			calendar.print();
			break;
		case 'Q':// 退出程序
		case 'q':
			cout<<"quit success!"<<endl;
			return 0;
		default:
			break;
		}
	}

	return 0;
}
