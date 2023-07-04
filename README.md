---------------------------------------------------------------------------------------------------------------------------------------------------
**Table of Contents**

- [Notes](#notes)
- [Dependencies](#dependencies)
- [Quick Start](#quickstart)
- [Settings](#settings)
- [Setting Up A MySQL Database](#SUAMSD)
- [License](#license)
- [Contact](#contact)

---------------------------------------------------------------------------------------------------------------------------------------------------
**Notes**<a name="notes"></a>

Built for Windows, Should work on Linux/MacOS but is untested.

Python Version: 3.8+

Tests the user on Japanese Kana.

Plans are in place to expand the program greatly.

---------------------------------------------------------------------------------------------------------------------------------------------------
**Dependencies**<a name="dependencies"></a>

mysql.connector-python

requests

or see requirements.txt

---------------------------------------------------------------------------------------------------------------------------------------------------
**Quick Start**<a name="quickstart"></a>

Run seisen.py

Upon opening the file, you will be prompted to enter database credentials, if you have these go ahead and enter these, otherwise enter z to skip.

Once at the main menu, press 1 and begin to quiz yourself on kana.

The average user will have no need to use the settings options unless they want to see the score ratings.

---------------------------------------------------------------------------------------------------------------------------------------------------
**Settings**<a name="settings"></a>

pressing 2 will enter the settings menu. The settings are as follows.

1. Reset Local Storage - this will reset your Local Storage with your Remote Storage (database), will do nothing if no database is present.
2. Reset Remote Storage - this will reset your Remote Storage with your Local Storage, will do nothing if no database is present.
3. See Score Ratings - this will print the likelihood of each kana being tested.
4. Add New Database - this will cause Seisen to prompt for a new database.
5. Restore Local Backup - this will cause Seisen to prompt the user to select an old Seisen Local Backup
6. Restore Remote Backup - this will cause Seisen to prompt the user to select an old Seisen Remote Backup
   
---------------------------------------------------------------------------------------------------------------------------------------------------
**Setting Up A MySQL Database**<a name="SUAMSD"></a>

Seisen uses a backup data method using MySQL, once Seisen is opened for the first time it will prompt for A database name and password, if you have these already feel free to enter these and Seisen will take care of the rest.

If not, you can always set this up latter in settings by typing 2 and then press 4.

---------------------------------------------------------------------------------------------------------------------------------------------------
**License**<a name="license"></a>

This project (Seisen) is licensed under the GNU General Public License (GPL). You can find the full text of the license in the [LICENSE](License.md) file.

The GPL is a copyleft license that promotes the principles of open-source software. It ensures that any derivative works based on this project must also be distributed under the same GPL license. This license grants you the freedom to use, modify, and distribute the software.

Please note that this information is a brief summary of the GPL. For a detailed understanding of your rights and obligations under this license, please refer to the full license text.

---------------------------------------------------------------------------------------------------------------------------------------------------
**Contact**<a name="contact"></a>

If you have any questions, comments, or concerns, please feel free to contact me at [Seinuve@gmail.com](mailto:Seinuve@gmail.com).

For any bugs or suggestions please use the issues tab [here](https://github.com/Seinuve/Seisen/issues).

---------------------------------------------------------------------------------------------------------------------------------------------------
