import sys
from PySide.QtCore import *
from PySide.QtGui import *
import irods
from irods.session import iRODSSession

qt_app = QApplication(sys.argv)

class IRODSAuthApplication(QWidget):

    def __init__(self):
        super(IRODSAuthApplication, self).__init__()

        self.current_path = ''
        self.setWindowTitle('iRODS Browser')
        self.irods_session = None
        # username inputs
        self.username_lbl = QLabel('Username:', self)
        self.username_txt = QLineEdit(self)
        self.error_msg = QErrorMessage(self)
        # password inputs
        self.password_lbl = QLabel('Password:', self)
        self.password_txt = QLineEdit(self)
        self.password_txt.setEchoMode(QLineEdit.Password)

        # irods zone, port, and server info
        self.irods_zone_lbl = QLabel('Zone:', self)
        self.irods_zone_txt = QLineEdit(self)
        self.irods_port_lbl = QLabel('Port:', self)
        self.irods_port_txt = QLineEdit('1247', self)
        self.irods_port_txt.setValidator(QIntValidator(1, 65535, self))
        self.irods_server_lbl = QLabel('Server:', self)
        self.irods_server_txt = QLineEdit(self)
        self.current_path_lbl = QLabel(self)
        self.current_path_lbl.hide()

        # login button
        self.login_button = QPushButton('Login', self)
        self.login_button.setMinimumWidth(130)
        self.login_button.clicked.connect(self.login_irods)

        # file tree
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(['Name', 'Last Modified', 'Size'])
        self.tree_widget.setColumnCount(3)
        self.tree_widget.itemActivated.connect(self.process_item)
        self.tree_widget.header().resizeSection(0, 200)
        self.tree_widget.header().resizeSection(1, 200)
        self.tree_widget.header().resizeSection(2, 100)
        self.tree_widget.hide()

        # cd up button
        self.cd_up_btn = QPushButton()
        self.cd_up_btn.setIcon(QIcon('/home/neddy/images/cdtoparent.png'))
        self.cd_up_btn.clicked.connect(self.cd_to_parent)
        self.cd_up_btn.setGeometry(30, 30, 30, 30)
        self.cd_up_btn.hide()
        self.current_path_lbl.setBuddy(self.cd_up_btn)

        # layouts
        self.login_layout = QFormLayout()
        self.login_layout.addRow(self.username_lbl, self.username_txt)
        self.login_layout.addRow(self.password_lbl, self.password_txt)
        self.login_layout.addRow(self.irods_zone_lbl, self.irods_zone_txt)
        self.login_layout.addRow(self.irods_port_lbl, self.irods_port_txt)
        self.login_layout.addRow(self.irods_server_lbl, self.irods_server_txt)
        self.login_layout.addRow(self.login_button)
        self.login_widget = QWidget()
        self.login_widget.setLayout(self.login_layout)

        self.info_layout = QHBoxLayout()
        self.info_layout.addWidget(self.current_path_lbl)
        self.info_layout.addWidget(self.cd_up_btn)
        self.info_widget = QWidget()
        self.info_widget.setLayout(self.info_layout)
        self.info_widget.hide()
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.login_widget)
        self.main_layout.addWidget(self.info_widget)
        self.main_layout.addWidget(self.tree_widget)
        self.setLayout(self.main_layout)

    def sizeHint(self):
        return QSize(250, 200)

    def run(self):
        self.show()
        qt_app.exec_()

    def login_irods(self):
        self.irods_session = iRODSSession(
                                          host=self.irods_server_txt.text().encode('ascii','xmlcharrefreplace'),
                                          port=int(self.irods_port_txt.text().encode('ascii')),
                                          user=self.username_txt.text().encode('ascii','xmlcharrefreplace'),
                                          password=self.password_txt.text().encode('ascii','xmlcharrefreplace'),
                                          zone=self.irods_zone_txt.text().encode('ascii','xmlcharrefreplace')
                                          )
        try:
            parent = self.irods_session.collections.get('/')
            self.current_path = parent.path
            self.current_path_lbl.setText(self.current_path)
            self.current_path_lbl.show()
            self.tree_widget.show()
            self.cd_up_btn.show()
            self.info_widget.show()
            self.login_widget.hide()
            parent_item = QTreeWidgetItem([parent.path])
            self.process_item(parent_item)
            self.cd_up_btn.setEnabled(False)
            self.resize(600, 400)
        except irods.exception.CAT_INVALID_AUTHENTICATION:
            self.error_msg.showMessage('Password invalid. Please try again.')
        except irods.exception.CAT_INVALID_USER:
            self.error_msg.showMessage('User invalid. Please try again.')
        except:
            self.error_msg.showMessage('Error logging in. Please try again.')

    def process_item(self, item, cd=False):
        if not cd:
            if self.is_directory(item):
                self.cd_up_btn.setEnabled(True)
                self.current_path_lbl.setText(self.current_path)
                self.tree_widget.clear()
                coll = self.irods_session.collections.get(self.current_path)
                for subcoll in coll.subcollections:
                    new_dir = QTreeWidgetItem(self.tree_widget)
                    new_dir.setText(0, subcoll.path.split('/')[len(subcoll.path.split('/'))-1])
                    new_dir.setIcon(0, QIcon('/home/neddy/images/dir.png'))
                    self.tree_widget.insertTopLevelItem(0, new_dir)
                for obj in coll.data_objects:
                    new_obj = QTreeWidgetItem(self.tree_widget)
                    new_obj.setText(0, obj.name)
                    new_obj.setText(1, str(obj.modify_time))
                    new_obj.setText(2, str(obj.size))
                    new_obj.setIcon(0, QIcon('/home/neddy/images/file.png'))
                    self.tree_widget.insertTopLevelItem(0, new_obj)
        else:
            self.current_path_lbl.setText(self.current_path)
            self.tree_widget.clear()
            coll = self.irods_session.collections.get(self.current_path)
            for subcoll in coll.subcollections:
                new_dir = QTreeWidgetItem(self.tree_widget)
                new_dir.setText(0, subcoll.path.split('/')[len(subcoll.path.split('/'))-1])
                new_dir.setIcon(0, QIcon('/home/neddy/images/dir.png'))
                self.tree_widget.insertTopLevelItem(0, new_dir)
            for obj in coll.data_objects:
                new_obj = QTreeWidgetItem(self.tree_widget)
                new_obj.setText(0, obj.name)
                new_obj.setText(1, str(obj.modify_time))
                new_obj.setText(2, str(obj.size))
                new_obj.setIcon(0, QIcon('/home/neddy/images/file.png'))
                self.tree_widget.insertTopLevelItem(0, new_obj)

    def is_directory(self, item):
        path = item.text(0).encode('ascii', 'xmlcharrefreplace')
        tmp = self.current_path
        if path != '/':
            if self.current_path != '/':
                self.current_path = self.current_path + '/' + path
                path = self.current_path + '/' + path
            else:
                self.current_path = self.current_path + path
                path = self.current_path + path
        try:
            self.irods_session.collections.get(self.current_path)
            return True
        except irods.exception.CollectionDoesNotExist:
            self.current_path = tmp
            return False

    def cd_to_parent(self):
        dirs = self.current_path.split('/')
        self.tree_widget.clear()
        if len(dirs) > 2:
            self.current_path = '/'.join(dirs[:-1])
        else:
            self.cd_up_btn.setEnabled(False)
            self.current_path = '/'
        self.process_item(QTreeWidgetItem([self.current_path]), True)

if __name__ == '__main__':
    app = IRODSAuthApplication()
    app.run()
