
-- DEPRECATED: not used

INSERT INTO project (code) VALUES ('admin');
INSERT INTO project (code) VALUES ('sthpw');
INSERT INTO project (code) VALUES ('unittest');


INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (10, 'sthpw/project', 'sthpw', 'Projects', 'sthpw', 'project', 'pyasm.biz.Project', 'Projects', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (103, 'sthpw/login', 'sthpw', 'List of users', 'sthpw', 'login', 'pyasm.security.Login', 'Users', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (68, 'sthpw/search_object', 'sthpw', 'List of all the search objects', 'sthpw', 'search_object', 'pyasm.search.SearchType', 'Search Objects', 'public');


INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (1, 'sthpw/annotation', 'sthpw', 'Image Annotations', 'sthpw', 'annotation', 'pyasm.search.search.SObject', 'Image Annotations', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (2, 'sthpw/retire_log', 'sthpw', 'Retire SObject log', 'sthpw', 'retire_log', 'pyasm.search.RetireLog', 'Retire SObject log', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (3, 'sthpw/login_in_group', 'sthpw', 'Users in groups', 'sthpw', 'login_in_group', 'pyasm.security.LoginInGroup', 'Users in groups', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (4, 'sthpw/exception_log', 'sthpw', 'Exception Log', 'sthpw', 'exception_log', 'pyasm.search.SObject', 'Exception Log', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (6, 'sthpw/file_access', 'sthpw', 'File Access Log', 'sthpw', 'file_access', 'pyasm.biz.FileAccess', 'File Access Log', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (7, 'sthpw/repo', 'sthpw', 'Repository List', 'sthpw', 'repo', 'pyasm.search.SObject', 'Repository List', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (8, 'sthpw/queue', 'sthpw', 'Tactic Dispatcher', 'sthpw', 'queue', 'pyasm.search.SObject', 'Tactic Dispatcher', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (11, 'sthpw/task', 'sthpw', 'User Tasks', 'sthpw', 'task', 'pyasm.biz.Task', 'User Tasks', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (12, 'sthpw/sobject_config', 'sthpw', 'SObject Config Data', 'sthpw', 'sobject_config', 'pyasm.search.SObjectDbConfig', 'SObject Config Data', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (14, 'sthpw/transaction_state', 'sthpw', 'XMLRPC State', 'sthpw', 'transaction_state', 'pyasm.search.TransactionState', 'transaction_state', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (15, 'sthpw/command', 'sthpw', 'Commands in Tactic', 'sthpw', 'command', 'pyasm.biz.CommandSObj', 'Commands in Tactic', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (16, 'sthpw/milestone', 'sthpw', 'Project Milestones', 'sthpw', 'milestone', 'pyasm.biz.Milestone', 'Project Milestones', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (17, 'prod/layer', 'prod', 'Layers', '{project}', '{public}.layer', 'pyasm.prod.biz.Layer', 'Layers', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (18, 'sthpw/schema', 'sthpw', 'Schema', 'sthpw', 'schema', 'pyasm.biz.Schema', 'Schema', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (19, 'prod/shot_texture', 'prod', 'Shot Texture maps', '{project}', '{public}.shot_texture', 'pyasm.prod.biz.ShotTexture', 'Shot Texture maps', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (20, 'prod/storyboard', 'prod', 'Storyboard', '{project}', '{public}.storyboard', 'pyasm.search.SObject', 'Storyboard', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (21, 'prod/episode', 'prod', 'Episode', '{project}', '{public}.episode', 'pyasm.prod.biz.Episode', 'Episode', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (22, 'prod/script', 'prod', 'Script', '{project}', '{public}.script', 'pyasm.search.SObject', 'Script', 'public');

INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (23, 'prod/asset_type', 'prod', 'Asset Type', '{project}', '{public}.asset_type', 'pyasm.search.SObject', 'Asset Type', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (24, 'prod/asset_library', 'prod', 'Asset Library Types', '{project}', '{public}.asset_library', 'pyasm.prod.biz.AssetLibrary', 'Asset Library Types', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (25, 'prod/node_data', 'prod', 'Maya Node Data', '{project}', 'node_data', 'pyasm.search.SObject', 'Maya Node Data', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (26, 'prod/texture_source', 'prod', 'Texture Source', '{project}', 'texture_source', 'pyasm.prod.biz.TextureSource', 'Texture Source', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (27, 'prod/leica', 'prod', 'Leica', '{project}', 'leica', 'pyasm.search.SObject', 'Leica', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (28, 'prod/render', 'prod', 'Renders', '{project}', 'render', 'pyasm.prod.biz.Render', 'Renders', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (36, 'prod/art_reference', 'prod', 'Reference Images', '{project}', 'art_reference', 'pyasm.search.SObject', 'Reference Images', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (37, 'prod/layer_instance', 'prod', 'An instance of an layer in a shot', '{project}', '{public}.layer_instance', 'pyasm.prod.biz.LayerInstance', 'An instance of an layer in a shot', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (38, 'prod/bin', 'prod', 'Bin for submissions', '{project}', 'bin', 'pyasm.prod.biz.Bin', 'Bin for submissions', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (39, 'prod/submission_in_bin', 'prod', 'Submissions in Bins', '{project}', 'submission_in_bin', 'pyasm.prod.biz.SubmissionInBin', 'Submissions in Bins', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (40, 'prod/prod_setting', 'prod', 'Production Settings', '{project}', 'prod_setting', 'pyasm.prod.biz.ProdSetting', 'Production Settings', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (41, 'prod/camera', 'prod', 'Camera Information', '{project}', 'camera', 'pyasm.search.SObject', 'Camera Information', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (45, 'game/texture', 'game', 'Game Texture', '{project}', 'texture', 'pyasm.game.biz.GameTexture', 'Game Texture', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (46, 'game/asset', 'game', 'Game Asset', '{project}', 'asset', 'pyasm.game.biz.GameAsset', 'Game Asset', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (47, 'game/level', 'game', 'Game Level', '{project}', 'level', 'pyasm.game.biz.GameLevel', 'Game Level', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (48, 'game/level_instance', 'game', 'Game Level Instance', '{project}', 'instance', 'pyasm.game.biz.GameLevelInstance', 'Game Level Instance', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (49, 'game/art_reference', 'game', 'Reference Images', '{project}', 'art_reference', 'pyasm.game.biz.GameArtReference', 'Reference Images', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (50, 'prod/asset', 'prod', 'The base atomic entity that can exist shot', '{project}', '{public}.asset', 'pyasm.prod.biz.Asset', '3D Asset', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (51, 'prod/sequence', 'prod', 'A list of shots that are grouped together', '{project}', '{public}.sequence', 'pyasm.prod.biz.Sequence', 'Sequence', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (52, 'prod/session_contents', 'prod', 'Introspection Contents of a users session', '{project}', 'session_contents', 'pyasm.prod.biz.SessionContents', 'Session Contents', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (53, 'prod/shot', 'prod', 'A camera cut', '{project}', '{public}.shot', 'pyasm.prod.biz.Shot', 'Shot', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (54, 'prod/shot_instance', 'prod', 'An instance of an asset in a shot', '{project}', '{public}.instance', 'pyasm.prod.biz.ShotInstance', 'Shot Instance', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (55, 'prod/submission', 'prod', 'Submission of quicktime, media files for an asset', '{project}', 'submission', 'pyasm.prod.biz.Submission', 'Submission', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (57, 'prod/render_stage', 'prod', 'Stages for specfic assets', '{project}', '{public}.render_stage', 'pyasm.search.SObject', 'Render Stage', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (58, 'sthpw/command_log', 'sthpw', 'Historical log of all of the commands executed', 'sthpw', 'command_log', 'pyasm.command.CommandLog', 'Command Log', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (59, 'sthpw/file', 'sthpw', 'A record of all files that are tracked', 'sthpw', 'file', 'pyasm.biz.file.File', 'File', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (60, 'sthpw/login_group', 'sthpw', 'List of groups that user belong to', 'sthpw', 'login_group', 'pyasm.security.LoginGroup', 'Groups', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (61, 'sthpw/note', 'sthpw', 'Notes', 'sthpw', 'note', 'pyasm.biz.Note', 'Notes', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (62, 'sthpw/pipeline', 'sthpw', 'List of piplines available for sobjects', 'sthpw', 'pipeline', 'pyasm.biz.Pipeline', 'Pipelines', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (63, 'sthpw/status_log', 'sthpw', 'Log of status changes', 'sthpw', 'status_log', 'pyasm.search.SObject', 'Status Log', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (64, 'sthpw/notification', 'sthpw', 'Different types of Notification', 'sthpw', 'notification', 'pyasm.biz.Notification', 'Notification', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (65, 'sthpw/group_notification', 'sthpw', 'Associate one of more kinds of notification with groups', 'sthpw', 'group_notification', 'pyasm.biz.GroupNotification', 'Group Notification', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (66, 'sthpw/snapshot', 'sthpw', 'All versions of snapshots of assets', 'sthpw', 'snapshot', 'pyasm.biz.Snapshot', 'Snapshot', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (67, 'sthpw/ticket', 'sthpw', 'Valid login tickets to enter the system', 'sthpw', 'ticket', 'pyasm.security.Ticket', 'Ticket', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (69, 'sthpw/wdg_settings', 'sthpw', 'Persistent store for widgets to remember user settings', 'sthpw', 'wdg_settings', 'pyasm.web.WidgetSettings', 'Widget Settings', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (70, 'sthpw/transaction_log', 'sthpw', NULL, 'sthpw', 'transaction_log', 'pyasm.search.TransactionLog', 'Transaction Log', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (71, 'sthpw/trigger_in_command', 'sthpw', 'Triggers contained in Command', 'sthpw', 'trigger_in_command', 'pyasm.biz.TriggerInCommand', 'Command Triggers', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (72, 'sthpw/sobject_log', 'sthpw', 'Log of actions on an sobject', 'sthpw', 'sobject_log', 'pyasm.search.SObject', 'SObject Log', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (73, 'sthpw/project_type', 'sthpw', 'Project Type', 'sthpw', 'project_type', 'pyasm.biz.ProjectType', 'Project Type', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (74, 'sthpw/pref_setting', 'sthpw', 'Preference Setting', 'sthpw', '{public}.pref_setting', 'pyasm.biz.PrefSetting', 'Pref Setting', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (75, 'sthpw/access_rule', 'sthpw', 'Access Rules', 'sthpw', '{public}.access_rule', 'pyasm.security.AccessRule', 'Access Rule', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (76, 'sthpw/access_rule_in_group', 'sthpw', 'Access Rules In Group', 'sthpw', '{public}.access_rule_in_group', 'pyasm.security.AccessRuleInGroup', '', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (77, 'sthpw/clipboard', 'sthpw', 'Clipboard', 'sthpw', '{public}.clipboard', 'pyasm.biz.Clipboard', '', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (78, 'sthpw/pref_list', 'sthpw', 'Preferences List', 'sthpw', '{public}.pref_list', 'pyasm.biz.PrefList', '', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (79, 'sthpw/translation', 'sthpw', 'Locale Translations', 'sthpw', '{public}.translation', 'pyasm.search.SObject', '', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (81, 'sthpw/notification_log', 'sthpw', 'Notification Log', 'sthpw', '{public}.notification_log', 'pyasm.search.SObject', 'Notification Log', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (82, 'sthpw/notification_login', 'sthpw', 'Notification Login', 'sthpw', '{public}.notification_login', 'pyasm.search.SObject', '', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (83, 'sthpw/timecard', 'sthpw', 'Timecard Registration', 'sthpw', 'timecard', 'pyasm.search.SObject', 'Timecard', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (85, 'sthpw/connection', 'sthpw', 'Connections', 'sthpw', 'connection', 'pyasm.biz.SObjectConnection', 'Connections', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (86, 'prod/cut_sequence', 'prod', 'Cut Sequences', '{project}', 'cut_sequence', 'pyasm.prod.biz.CutSequence', 'Cut Sequences', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (87, 'prod/naming', 'prod', 'Naming', '{project}', '{public}.naming', 'pyasm.biz.Naming', '', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (88, 'sthpw/remote_repo', 'sthpw', 'Remote Repositories', 'sthpw', 'remote_repo', 'pyasm.biz.RemoteRepo', 'Remote Repositories', NULL);
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (89, 'sthpw/widget_extend', 'sthpw', 'Extend Widget', 'sthpw', 'widget_extend', 'pyasm.search.SObject', 'widget_extend', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (90, 'prod/plate', 'prod', 'Production Plates', '{project}', 'plate', 'pyasm.search.SObject', 'Production plates', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (91, 'sthpw/search_type', 'sthpw', 'List of all the search objects', 'sthpw', 'search_object', 'pyasm.search.SearchType', 'Search Objects', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (92, 'sthpw/snapshot_type', 'sthpw', 'Snapshot Type', 'sthpw', 'snapshot_type', 'pyasm.biz.SnapshotType', 'Snapshot Type', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (93, 'game/beat', 'game', 'Beat', '{project}', 'beat', 'pyasm.search.SObject', 'Beat', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (94, 'game/take', 'game', 'Take', '{project}', 'take', 'pyasm.search.SObject', 'Take', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (95, 'sthpw/widget_config', 'sthpw', 'Widget Config Data', 'sthpw', 'widget_config', 'pyasm.search.WidgetDbConfig', 'Widget Config Data', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (96, 'sthpw/debug_log', 'sthpw', 'Debug Log', 'sthpw', 'debug_log', 'pyasm.biz.DebugLog', 'Debug Log', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (97, 'prod/custom_property', 'sthpw', 'Custom Property', '{project}', 'custom_property', 'pyasm.biz.CustomProperty', 'Custom Property', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (98, 'unittest/person', 'unittest', 'Unittest Person', 'unittest', 'person', 'pyasm.search.SObject', 'Unittest Person', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (99, 'unittest/city', 'unittest', 'Unittest City', 'unittest', 'city', 'pyasm.search.SObject', 'Unittest City', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (100, 'unittest/country', 'unittest', 'Unittest Country', 'unittest', 'country', 'pyasm.search.SObject', 'Unittest Country', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (101, 'prod/composite', 'prod', 'Composites', '{project}', '{public}.composite', 'pyasm.prod.biz.Composite', 'Composites', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (102, 'prod/texture', 'prod', 'Textures', '{project}', '{public}.texture', 'pyasm.prod.biz.Texture', 'Textures', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (103, 'sthpw/login', 'sthpw', 'List of users', 'sthpw', 'login', 'pyasm.security.Login', 'Users', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (104, 'sthpw/trigger', 'sthpw', 'Triggers', 'sthpw', 'trigger', 'pyasm.biz.TriggerSObj', 'Triggers', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (105, 'prod/snapshot_type', 'prod', 'Snapshot Type', '{project}', 'snapshot_type', 'pyasm.biz.SnapshotType', 'Snapshot Type', 'public');
INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (106, 'prod/render_policy', 'prod', 'Render Policy', '{project}', 'render_policy', 'pyasm.prod.biz.RenderPolicy', 'Render Policy', 'public');



INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (108, 'config/widget_config', 'config', 'Widget Config', '{project}', 'widget_config', 'pyasm.search.WidgetDbConfig', 'Widget Config', 'public');

INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (109, 'config/custom_script', 'config', 'Custom Script', '{project}', 'custom_script', 'pyasm.search.SObject', 'Custom Script', 'public');

INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (110, 'config/naming', 'config', 'Naming', '{project}', '{public}.naming', 'pyasm.biz.Naming', '', 'public');

INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (111, 'sthpw/cache', 'sthpw', 'Cache', 'sthpw', '{public}.cache', 'pyasm.search.SObject', '', 'public');

INSERT INTO search_object (id, search_type, namespace, description, "database", table_name, class_name, title, "schema") VALUES (112, 'config/prod_setting', 'config', 'Production Settings', '{project}', 'prod_setting', 'pyasm.prod.biz.ProdSetting', 'Production Settings', 'public');

INSERT INTO "search_object" ("id", "search_type", "namespace", "description", "database", "table_name", "class_name", "title", "schema") VALUES (113, 'config/client_trigger', 'config', 'Client Trigger', '{project}', 'spt_client_trigger', 'pyasm.search.SObject', 'Client Trigger', 'public'); 

INSERT INTO "search_object" ("id", "search_type", "namespace", "description", "database", "table_name", "class_name", "title", "schema") VALUES (114, 'config/url', 'config', 'Custom URL', '{project}', 'spt_url', 'pyasm.search.SObject', 'Custom URL', 'public'); 


INSERT INTO "search_object" ("id", "search_type", "namespace", "description", "database", "table_name", "class_name", "title", "schema") VALUES (115, 'config/plugin', 'config', 'Plugin', '{project}', 'spt_plugin', 'pyasm.search.SObject', 'Plugin', 'public'); 

INSERT INTO "search_object" ("id", "search_type", "namespace", "description", "database", "table_name", "class_name", "title", "schema") VALUES (116, 'config/trigger', 'config', 'Triggers', '{project}', 'spt_trigger', 'pyasm.biz.TriggerSObj', 'Triggers', 'public');

INSERT INTO "search_object" ("id", "search_type", "namespace", "description", "database", "table_name", "class_name", "title", "schema") VALUES (117, 'config/process', 'config', 'Processes', '{project}', 'spt_process', 'pyasm.search.SObject', 'Processes', 'public');

INSERT INTO "search_object" ("id", "search_type", "namespace", "description", "database", "table_name", "class_name", "title", "schema") VALUES (118, 'sthpw/work_hour', 'sthpw', 'Work Hours', 'sthpw', 'work_hour', 'pyasm.biz.WorkHour', 'Work Hours', 'public');

INSERT INTO "search_object" ("id", "search_type", "namespace", "description", "database", "table_name", "class_name", "title", "schema") VALUES (119, 'sthpw/custom_script', 'sthpw', 'Site Custom Script', 'sthpw', 'custom_script', 'pyasm.search.SObject', 'Global Custom Script', 'public');
