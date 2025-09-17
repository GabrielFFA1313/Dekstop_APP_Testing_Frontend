# NAVIGATION_ROUTER.PY - Router-based navigation system with JSON limiter and permission validation
import json
import os
from datetime import datetime, timedelta
from PyQt6.QtCore import QDate, QTime


class NavigationRouter:
    """Router class for managing view navigation and state using JSON with size limits and permission validation"""
    
    def __init__(self, main_app, json_file_path="navigation_state.json"):
        self.main_app = main_app
        self.json_file_path = json_file_path
        self.current_route = None
        self.navigation_history = []
        self.view_states = {}
        
        # JSON file size limits (in bytes)
        self.MAX_FILE_SIZE = 500 * 1024  # 500KB
        self.MAX_HISTORY_ITEMS = 20
        self.MAX_VIEW_STATES = 10        # Limit stored view states
        self.CLEANUP_DAYS = 2            # Remove history older than 2 days
        
        self.load_navigation_state()
    
    def get_user_permissions(self):
        """Get current user role and permissions"""
        user_role = getattr(self.main_app, 'user_role', '').lower()
        
        permissions = {
            'can_add_events': user_role in ['admin', 'administrator', 'super_admin', 'org', 'organization', 'faculty'],
            'can_edit_events': user_role in ['admin', 'administrator', 'super_admin'],
            'can_delete_events': user_role in ['admin', 'administrator', 'super_admin'],
            'restricted_views': []
        }
        
        # Define restricted views based on role
        if user_role in ['student']:
            permissions['restricted_views'] = ['add_event', 'edit_event']
        elif user_role in ['org', 'organization', 'faculty']:
            permissions['restricted_views'] = ['edit_event']  # Can add but not edit
        # Admin has no restrictions
        
        return permissions
    
    def is_view_allowed(self, view_name):
        """Check if current user can access the specified view"""
        permissions = self.get_user_permissions()
        return view_name not in permissions['restricted_views']
    
    def get_default_view_for_user(self):
        """Get default view based on user role"""
        user_role = getattr(self.main_app, 'user_role', '').lower()
        
        # All users can access calendar as default
        return 'calendar'
    
    def validate_and_sanitize_route(self, route):
        """Validate route against current user permissions and sanitize if needed"""
        if not route or 'view' not in route:
            return {'view': self.get_default_view_for_user(), 'params': {}}
        
        view_name = route['view']
        
        # Check if user can access this view
        if not self.is_view_allowed(view_name):
            return {'view': self.get_default_view_for_user(), 'params': {}}
        
        return route
    
    def cleanup_old_data(self):
        """Clean up old navigation history and view states to prevent JSON bloat"""
        try:
            # Remove old history items
            if self.navigation_history:
                cutoff_date = datetime.now() - timedelta(days=self.CLEANUP_DAYS)
                self.navigation_history = [
                    item for item in self.navigation_history
                    if datetime.fromisoformat(item['timestamp']) > cutoff_date
                ]
            
            # Limit history size
            if len(self.navigation_history) > self.MAX_HISTORY_ITEMS:
                self.navigation_history = self.navigation_history[-self.MAX_HISTORY_ITEMS:]
            
            # Limit view states (keep only recent ones)
            if len(self.view_states) > self.MAX_VIEW_STATES:
                # Keep only the most commonly used views
                priority_views = ['calendar', 'day_view', 'activities']
                filtered_states = {}
                
                # Keep priority views first
                for view in priority_views:
                    if view in self.view_states:
                        filtered_states[view] = self.view_states[view]
                
                # Add remaining views up to limit
                remaining_count = self.MAX_VIEW_STATES - len(filtered_states)
                for view, state in list(self.view_states.items()):
                    if view not in filtered_states and remaining_count > 0:
                        filtered_states[view] = state
                        remaining_count -= 1
                
                self.view_states = filtered_states
            
        except Exception as e:
            pass  # Error during cleanup
    
    def check_file_size(self):
        """Check if JSON file exceeds size limit"""
        try:
            if os.path.exists(self.json_file_path):
                file_size = os.path.getsize(self.json_file_path)
                if file_size > self.MAX_FILE_SIZE:
                    self.cleanup_old_data()
                    return True
            return False
        except Exception as e:
            return False
    
    def load_navigation_state(self):
        """Load navigation state from JSON file with permission validation"""
        try:
            if os.path.exists(self.json_file_path):
                # Check file size before loading
                self.check_file_size()
                
                with open(self.json_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Load and deserialize current_route
                current_route_data = data.get('current_route', {
                    'view': 'calendar',
                    'params': {}
                })
                loaded_route = {
                    'view': current_route_data['view'],
                    'params': self._deserialize_view_state(current_route_data.get('params', {}))
                }
                
                # SECURITY FIX: Validate loaded route against current user permissions
                self.current_route = self.validate_and_sanitize_route(loaded_route)
                
                # Load and deserialize navigation_history
                history_data = data.get('navigation_history', [])
                self.navigation_history = []
                for history_item in history_data:
                    # Only load history items that are valid for current user
                    if self.is_view_allowed(history_item['view']):
                        deserialized_item = {
                            'view': history_item['view'],
                            'params': self._deserialize_view_state(history_item.get('params', {})),
                            'timestamp': history_item['timestamp']
                        }
                        self.navigation_history.append(deserialized_item)
                
                # Load and deserialize view_states (only for allowed views)
                states_data = data.get('view_states', {})
                self.view_states = {}
                for view, state in states_data.items():
                    if self.is_view_allowed(view):
                        self.view_states[view] = self._deserialize_view_state(state)
                
                # Clean up old data after loading
                self.cleanup_old_data()
                
            else:
                # Initialize with default route
                self.current_route = {
                    'view': self.get_default_view_for_user(),
                    'params': {}
                }
                self.navigation_history = []
                self.view_states = {}
                
        except Exception as e:
            # Fallback to safe defaults
            self.current_route = {'view': self.get_default_view_for_user(), 'params': {}}
            self.navigation_history = []
            self.view_states = {}
    
    def save_navigation_state(self):
        """Save navigation state to JSON file with size monitoring"""
        try:
            # Clean up before saving
            self.cleanup_old_data()
            
            # Convert QDate and QTime objects to strings for JSON serialization
            serializable_states = {}
            for view, state in self.view_states.items():
                serializable_states[view] = self._serialize_view_state(state)
            
            # Serialize current_route params
            serialized_current_route = {
                'view': self.current_route['view'],
                'params': self._serialize_view_state(self.current_route['params'])
            }
            
            # Serialize navigation_history
            serialized_history = []
            for history_item in self.navigation_history:
                serialized_item = {
                    'view': history_item['view'],
                    'params': self._serialize_view_state(history_item['params']),
                    'timestamp': history_item['timestamp']
                }
                serialized_history.append(serialized_item)
            
            navigation_data = {
                'current_route': serialized_current_route,
                'navigation_history': serialized_history,
                'view_states': serializable_states,
                'metadata': {
                    'last_updated': datetime.now().isoformat(),
                    'app_version': '1.0',
                    'user_role': getattr(self.main_app, 'user_role', 'unknown'),
                    'data_stats': {
                        'history_count': len(serialized_history),
                        'view_states_count': len(serializable_states)
                    }
                }
            }
            
            # Create a backup if file exists and is large
            if os.path.exists(self.json_file_path):
                file_size = os.path.getsize(self.json_file_path)
                if file_size > self.MAX_FILE_SIZE * 0.8:  # 80% of max size
                    backup_path = f"{self.json_file_path}.backup"
                    try:
                        os.rename(self.json_file_path, backup_path)
                    except Exception as backup_error:
                        pass  # Could not create backup
            
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(navigation_data, file, indent=2, ensure_ascii=False)
            
            # Check file size after saving
            final_size = os.path.getsize(self.json_file_path)
            
            return True
            
        except Exception as e:
            return False
    
    def _serialize_view_state(self, state):
        """Convert PyQt objects to JSON-serializable format with size optimization"""
        if not isinstance(state, dict):
            return state
            
        serialized = {}
        for key, value in state.items():
            if isinstance(value, QDate):
                serialized[key] = value.toString("yyyy-MM-dd")
            elif isinstance(value, QTime):
                serialized[key] = value.toString("hh:mm")
            elif isinstance(value, dict):
                serialized[key] = self._serialize_view_state(value)
            elif isinstance(value, str) and len(value) > 1000:  # Limit long strings
                serialized[key] = value[:1000] + "..." if len(value) > 1000 else value
            else:
                serialized[key] = value
        
        return serialized
    
    def _deserialize_view_state(self, state):
        """Convert JSON data back to PyQt objects"""
        if not isinstance(state, dict):
            return state
            
        deserialized = {}
        for key, value in state.items():
            if key.endswith('_date') and isinstance(value, str):
                deserialized[key] = QDate.fromString(value, "yyyy-MM-dd")
            elif key.endswith('_time') and isinstance(value, str):
                deserialized[key] = QTime.fromString(value, "hh:mm")
            elif isinstance(value, dict):
                deserialized[key] = self._deserialize_view_state(value)
            else:
                deserialized[key] = value
        
        return deserialized
    
    def navigate_to(self, view_name, params=None, save_current=True):
        """Navigate to a specific view with permission validation"""
        if params is None:
            params = {}
        
        try:
            # SECURITY CHECK: Validate permissions before navigation
            if not self.is_view_allowed(view_name):
                # Show warning and redirect to default view
                try:
                    from PyQt6.QtWidgets import QMessageBox
                    QMessageBox.warning(
                        self.main_app,
                        "Access Denied",
                        f"You do not have permission to access this view.\nRedirecting to the main calendar."
                    )
                except:
                    pass  # If QMessageBox fails, just continue
                
                # Redirect to default view
                view_name = self.get_default_view_for_user()
                params = {}
            
            # Save current view state before navigating
            if save_current and self.current_route:
                self._save_current_view_state()
                
                # Add to navigation history (only if view is allowed)
                if self.is_view_allowed(self.current_route['view']):
                    self.navigation_history.append({
                        'view': self.current_route['view'],
                        'params': self.current_route['params'].copy(),
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    # Limit history size immediately
                    if len(self.navigation_history) > self.MAX_HISTORY_ITEMS:
                        self.navigation_history = self.navigation_history[-self.MAX_HISTORY_ITEMS:]
            
            # Update current route
            self.current_route = {
                'view': view_name,
                'params': params.copy()
            }
            
            # Clean up before saving
            self.cleanup_old_data()
            
            # Save navigation state
            self.save_navigation_state()
            
            # Perform the actual view switch
            self._switch_to_view(view_name, params)
            
            return True
            
        except Exception as e:
            return False
    
    def go_back(self):
        """Navigate back to the previous view with permission validation"""
        if not self.navigation_history:
            return False
        
        try:
            # Get the last route from history
            previous_route = self.navigation_history.pop()
            
            # Validate permissions for the previous route
            if not self.is_view_allowed(previous_route['view']):
                previous_route = {'view': self.get_default_view_for_user(), 'params': {}}
            
            # Navigate without adding to history (to avoid loop)
            return self.navigate_to(
                previous_route['view'],
                previous_route['params'],
                save_current=False
            )
            
        except Exception as e:
            return False
    
    def get_navigation_history(self):
        """Get the navigation history (filtered by permissions)"""
        filtered_history = [
            item for item in self.navigation_history 
            if self.is_view_allowed(item['view'])
        ]
        return filtered_history
    
    def clear_history(self):
        """Clear navigation history"""
        self.navigation_history = []
        self.save_navigation_state()
    
    def force_cleanup(self):
        """Force cleanup of old data (can be called manually)"""
        original_history_count = len(self.navigation_history)
        original_states_count = len(self.view_states)
        
        self.cleanup_old_data()
        self.save_navigation_state()
    
    def get_json_file_stats(self):
        """Get statistics about the JSON file"""
        stats = {
            'file_exists': os.path.exists(self.json_file_path),
            'file_size': 0,
            'max_size': self.MAX_FILE_SIZE,
            'history_count': len(self.navigation_history),
            'view_states_count': len(self.view_states)
        }
        
        if stats['file_exists']:
            try:
                stats['file_size'] = os.path.getsize(self.json_file_path)
                stats['size_percentage'] = (stats['file_size'] / self.MAX_FILE_SIZE) * 100
            except Exception as e:
                pass  # Error getting file stats
        
        return stats
    
    def _save_current_view_state(self):
        """Save the current view's state with size limits"""
        current_view = self.current_route['view']
        
        # Don't save state for restricted views
        if not self.is_view_allowed(current_view):
            return
        
        # Collect view-specific state
        view_state = {}
        
        if current_view == 'calendar':
            view_state = self._get_calendar_state()
        elif current_view == 'day_view':
            view_state = self._get_day_view_state()
        elif current_view == 'activities':
            view_state = self._get_activities_state()
        elif current_view == 'add_event' or current_view == 'edit_event':
            view_state = self._get_event_form_state()
        
        # Store in view_states with size limit
        if view_state:
            self.view_states[current_view] = view_state
            
            # Enforce view states limit
            if len(self.view_states) > self.MAX_VIEW_STATES:
                # Remove oldest non-priority view state
                priority_views = ['calendar', 'day_view', 'activities']
                for view in list(self.view_states.keys()):
                    if view not in priority_views:
                        del self.view_states[view]
                        break
    
    def _get_calendar_state(self):
        """Get calendar view state"""
        state = {}
        if hasattr(self.main_app, 'calendar_ui') and self.main_app.calendar_ui:
            if hasattr(self.main_app.calendar_ui, 'calendarWidget'):
                state['selected_date'] = self.main_app.calendar_ui.calendarWidget.selectedDate()
            if hasattr(self.main_app.calendar_ui, 'comboUpcomingFilter'):
                state['filter_selection'] = self.main_app.calendar_ui.comboUpcomingFilter.currentText()
        return state
    
    def _get_day_view_state(self):
        """Get day view state"""
        state = {}
        if hasattr(self.main_app, 'current_date'):
            state['current_date'] = self.main_app.current_date
        if hasattr(self.main_app, 'day_view_manager') and self.main_app.day_view_manager.day_view_ui:
            if hasattr(self.main_app.day_view_manager.day_view_ui, 'comboUpcomingFilter'):
                state['filter_selection'] = self.main_app.day_view_manager.day_view_ui.comboUpcomingFilter.currentText()
        return state
    
    def _get_activities_state(self):
        """Get activities view state"""
        state = {}
        if hasattr(self.main_app, 'activities_manager') and self.main_app.activities_manager.activities_ui:
            if hasattr(self.main_app.activities_manager.activities_ui, 'comboActivityType'):
                state['activity_filter'] = self.main_app.activities_manager.activities_ui.comboActivityType.currentText()
            if hasattr(self.main_app.activities_manager.activities_ui, 'comboUpcomingFilter'):
                state['upcoming_filter'] = self.main_app.activities_manager.activities_ui.comboUpcomingFilter.currentText()
        return state
    
    def _get_event_form_state(self):
        """Get event form state (minimal for security)"""
        state = {}
        # We don't save form data for security/privacy reasons
        # But we can save form metadata
        if hasattr(self.main_app, 'add_event_manager'):
            state['mode'] = getattr(self.main_app.add_event_manager, 'mode', 'add')
        return state
    
    def _switch_to_view(self, view_name, params):
        """Actually switch to the specified view"""
        # Clear current central widget
        self.main_app.setCentralWidget(None)
        
        # Force garbage collection
        import gc
        gc.collect()
        
        # Restore view state if available
        saved_state = self.view_states.get(view_name, {})
        if saved_state:
            saved_state = self._deserialize_view_state(saved_state)
        
        # Switch to the appropriate view using main app's create methods
        if view_name == 'calendar':
            self.main_app.create_calendar_view(params, saved_state)
        elif view_name == 'day_view':
            self.main_app.create_day_view(params, saved_state)
        elif view_name == 'activities':
            self.main_app.create_activities_view(params, saved_state)
        elif view_name == 'add_event':
            self.main_app.create_add_event_view(params, saved_state)
        elif view_name == 'edit_event':
            self.main_app.create_edit_event_view(params, saved_state)
        elif view_name == 'search':
            self.main_app.create_search_view(params, saved_state)
        else:
            raise ValueError(f"Unknown view: {view_name}")
    
    # Convenience methods for common navigation patterns (with permission checks)
    def to_calendar(self, selected_date=None):
        """Navigate to calendar view"""
        params = {}
        if selected_date:
            params['selected_date'] = selected_date
        return self.navigate_to('calendar', params)
    
    def to_day_view(self, date=None):
        """Navigate to day view"""
        params = {}
        if date:
            params['date'] = date
        return self.navigate_to('day_view', params)
    
    def to_activities(self):
        """Navigate to activities view"""
        return self.navigate_to('activities')
    
    def to_add_event(self):
        """Navigate to add event view (with permission check)"""
        return self.navigate_to('add_event')
    
    def to_edit_event(self, event_data):
        """Navigate to edit event view (with permission check)"""
        return self.navigate_to('edit_event', {'event_data': event_data})
    
    def to_search(self, query=''):
        """Navigate to search view"""
        return self.navigate_to('search', {'query': query})
    
    def get_current_route(self):
        """Get the current route information"""
        return self.current_route.copy()
    
    def is_current_view(self, view_name):
        """Check if the specified view is currently active"""
        return self.current_route['view'] == view_name