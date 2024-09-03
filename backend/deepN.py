
def create_model(X,y, X_test, y_test):
    #X = StandardScaler().fit_transform(X)
    #y = StandardScaler().fit_transform(y.reshape(len(y),1))[:,0]
    #X_test = StandardScaler().fit_transform(X_test)
    #y_test = StandardScaler().fit_transform(y_test.reshape(len(y_test),1))[:,0]

    # Set random seed
    tf.random.set_seed(96)
    nbFeatures = X.columns.size
        # Create a model using the Sequential API
    model=Sequential() #here we get an insance of our model
    model.add(Dense(nbFeatures, activation="relu")) # here we add a dense layer with 19 neurons because we have 19 features
    model.add(Dense(nbFeatures, activation="relu")) # here we add a dense layer with 19 neurons because we have 19 features
    model.add(Dense(nbFeatures, activation="relu")) # here we add a dense layer with 19 neurons because we have 19 features
    model.add(Dense(nbFeatures, activation="relu")) # here we add a dense layer with 19 neurons because we have 19 features
    model.add(Dense(nbFeatures, activation="relu")) # here we add a dense layer with 19 neurons because we have 19 features
    model.add(Dense(nbFeatures, activation="relu")) # here we add a dense layer with 19 neurons because we have 19 features
    model.add(Dense(1, activation="linear")) # here we add add the final layer with 1 neurons because we have one output, that is the house price
    # Compile the model
    #loss_fn = keras.losses.MeanSquaredError(reduction='sum_over_batch_size')
    #tf.keras.optimizers.Adam(), # SGD is short for stochastic gradient descent
    #loss_fn = tf.keras.losses.MeanSquaredError() # mae is short for mean absolute error
    loss_fn = 'mean_absolute_error';
    opt = SGD(lr=0.01, momentum=0.9)
    model.compile(loss=loss_fn, # mae is short for mean absolute error
                optimizer=opt,
                metrics=["mae", "mse"])

    # Fit the model
    # model.fit(X, y, epochs=5) # this will break with TensorFlow 2.7.0+
    
    model.fit(x= X, y= y, batch_size=30, epochs=100, validation_data=(X_test, y_test))
    return model