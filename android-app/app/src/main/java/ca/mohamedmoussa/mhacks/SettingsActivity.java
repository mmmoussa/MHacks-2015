package ca.mohamedmoussa.mhacks;

import android.app.Activity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.CheckBox;

import com.firebase.client.DataSnapshot;
import com.firebase.client.Firebase;
import com.firebase.client.FirebaseError;
import com.firebase.client.ValueEventListener;

public class SettingsActivity extends Activity {

    Firebase myFirebaseRef;
    CheckBox walmartBox;
    CheckBox atmBox;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        walmartBox = (CheckBox) findViewById(R.id.walmart);
        atmBox = (CheckBox) findViewById(R.id.atm);

        Firebase.setAndroidContext(this);
        myFirebaseRef = new Firebase("https://MYLINK.firebaseio.com/");
        myFirebaseRef.child("capitalOne").addValueEventListener(new ValueEventListener() {

            @Override
            public void onDataChange(DataSnapshot snapshot) {
                if (snapshot.getValue().toString().equals("True")) {
                    atmBox.setChecked(true);
                } else {
                    atmBox.setChecked(false);
                }
            }

            @Override
            public void onCancelled(FirebaseError error) {
                System.out.println(error.getMessage());
            }

        });

        myFirebaseRef.child("walmart").addValueEventListener(new ValueEventListener() {

            @Override
            public void onDataChange(DataSnapshot snapshot) {
                if (snapshot.getValue().toString().equals("True")) {
                    walmartBox.setChecked(true);
                } else {
                    walmartBox.setChecked(false);
                }
            }

            @Override
            public void onCancelled(FirebaseError error) {
                System.out.println(error.getMessage());
            }

        });
    }

    public void save(View view) {
        if (walmartBox.isChecked()) {
            myFirebaseRef.child("walmart").setValue("True");
        } else {
            myFirebaseRef.child("walmart").setValue("False");
        }

        if (atmBox.isChecked()) {
            myFirebaseRef.child("capitalOne").setValue("True");
        } else {
            myFirebaseRef.child("capitalOne").setValue("False");
        }

        finish();
    }
}
