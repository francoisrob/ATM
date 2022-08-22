-- -----------------------------------------------------
-- SQL code to create db_atm
-- -----------------------------------------------------
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema db_ATM
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_ATM` DEFAULT CHARACTER SET utf8mb4 ;
USE `db_ATM` ;

-- -----------------------------------------------------
-- Table `db_ATM`.`tbl_users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_ATM`.`tbl_users` ;

CREATE TABLE IF NOT EXISTS `db_ATM`.`tbl_users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(45) NOT NULL,
  `sname` VARCHAR(45) NOT NULL,
  `street` VARCHAR(45) NOT NULL,
  `city` VARCHAR(45) NOT NULL,
  `state` VARCHAR(3) NOT NULL,
  `post` VARCHAR(4) NOT NULL,
  `cell_num` VARCHAR(10) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `id_num` VARCHAR(13) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_ATM`.`tbl_accounts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_ATM`.`tbl_accounts` ;

CREATE TABLE IF NOT EXISTS `db_ATM`.`tbl_accounts` (
  `acc_ID` INT NOT NULL AUTO_INCREMENT,
  `acc_balance` DECIMAL(13,2) NOT NULL,
  `date_created` DATE NOT NULL,
  `acc_type` CHAR(1) NOT NULL,
  `tbl_users_user_id` INT NOT NULL,
  `credit_due` DECIMAL(13,2) NOT NULL,
  PRIMARY KEY (`acc_ID`, `tbl_users_user_id`),
  INDEX `fk_tbl_accounts_tbl_users_idx` (`tbl_users_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_tbl_accounts_tbl_users`
    FOREIGN KEY (`tbl_users_user_id`)
    REFERENCES `db_ATM`.`tbl_users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_ATM`.`tbl_transactions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_ATM`.`tbl_transactions` ;

CREATE TABLE IF NOT EXISTS `db_ATM`.`tbl_transactions` (
  `trans_id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(100) NOT NULL,
  `amount` DECIMAL(13,2) NOT NULL,
  `date` DATETIME NOT NULL,
  `tbl_accounts_acc_ID` INT NOT NULL,
  `tbl_accounts_tbl_users_user_id` INT NOT NULL,
  PRIMARY KEY (`trans_id`, `tbl_accounts_acc_ID`, `tbl_accounts_tbl_users_user_id`),
  INDEX `fk_tbl_transactions_tbl_accounts1_idx` (`tbl_accounts_acc_ID` ASC, `tbl_accounts_tbl_users_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_tbl_transactions_tbl_accounts1`
    FOREIGN KEY (`tbl_accounts_acc_ID` , `tbl_accounts_tbl_users_user_id`)
    REFERENCES `db_ATM`.`tbl_accounts` (`acc_ID` , `tbl_users_user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- tbl_users insert
-- -----------------------------------------------------
INSERT INTO `db_atm`.`tbl_users` (`user_id`, `fname`, `sname`, `street`, `city`, `state`, `post`, `cell_num`, `email`, `id_num`, `username`, `password`) VALUES ('1', 'John', 'Smith', 'Curry', 'Cape Town', 'wc', '7100', '0923435566', 'jsmith@gmail.com', '9409205699083', 'js', '1234');
INSERT INTO `db_atm`.`tbl_users` (`user_id`, `fname`, `sname`, `street`, `city`, `state`, `post`, `cell_num`, `email`, `id_num`, `username`, `password`) VALUES ('2', 'Jane', 'Connor', 'Burger', 'Pretoria', 'gp', '0043', '0924546687', 'jconnor@gmail.com', '8511044499088', 'jc', '1234');
INSERT INTO `db_atm`.`tbl_users` (`user_id`, `fname`, `sname`, `street`, `city`, `state`, `post`, `cell_num`, `email`, `id_num`, `username`, `password`) VALUES ('3', 'Bob', 'Small', 'Pizza', 'Polokwane', 'lp', '0699', '0916784443', 'bsmall@gmail.com', '8801056991083', 'bs', '1234');

-- -----------------------------------------------------
-- tbl_accounts insert
-- -----------------------------------------------------
INSERT INTO `db_atm`.`tbl_accounts` (`acc_ID`, `acc_balance`, `date_created`, `acc_type`, `tbl_users_user_id`, `credit_due`) VALUES ('100', '5602.22', '2012-10-20', 'd', '1', '0.00');
INSERT INTO `db_atm`.`tbl_accounts` (`acc_ID`, `acc_balance`, `date_created`, `acc_type`, `tbl_users_user_id`, `credit_due`) VALUES ('101', '24000.00', '2013-03-02', 'c', '1', '1000.00');
INSERT INTO `db_atm`.`tbl_accounts` (`acc_ID`, `acc_balance`, `date_created`, `acc_type`, `tbl_users_user_id`, `credit_due`) VALUES ('102', '4300.05', '2010-05-03', 'd', '2', '0');
INSERT INTO `db_atm`.`tbl_accounts` (`acc_ID`, `acc_balance`, `date_created`, `acc_type`, `tbl_users_user_id`, `credit_due`) VALUES ('103', '55000.00', '2012-01-26', 's', '3', '0');
INSERT INTO `db_atm`.`tbl_accounts` (`acc_ID`, `acc_balance`, `date_created`, `acc_type`, `tbl_users_user_id`, `credit_due`) VALUES ('104', '15000.65', '2014-06-12', 's', '1', '0');

-- -----------------------------------------------------
-- tbl_transactions insert
-- -----------------------------------------------------
INSERT INTO `db_atm`.`tbl_transactions` (`trans_id`, `description`, `amount`, `date`, `tbl_accounts_acc_ID`, `tbl_accounts_tbl_users_user_id`) VALUES ('1', 'Steri Stumpi 100L', '-1000.00', '2022-04-05', '101', '1');
INSERT INTO `db_atm`.`tbl_transactions` (`trans_id`, `description`, `amount`, `date`, `tbl_accounts_acc_ID`, `tbl_accounts_tbl_users_user_id`) VALUES ('2', 'Bread and milk', '-30.99', '2022-04-02', '100', '1');
INSERT INTO `db_atm`.`tbl_transactions` (`trans_id`, `description`, `amount`, `date`, `tbl_accounts_acc_ID`, `tbl_accounts_tbl_users_user_id`) VALUES ('3', 'Income STOCKMARKET', '11000.00', '2022-04-03', '100', '1');
INSERT INTO `db_atm`.`tbl_transactions` (`trans_id`, `description`, `amount`, `date`, `tbl_accounts_acc_ID`, `tbl_accounts_tbl_users_user_id`) VALUES ('4', 'Income Mcdonalds', '16500.00', '2022-04-28', '102', '2');
INSERT INTO `db_atm`.`tbl_transactions` (`trans_id`, `description`, `amount`, `date`, `tbl_accounts_acc_ID`, `tbl_accounts_tbl_users_user_id`) VALUES ('5', 'x4 Tires Car shop', '-3600.00', '2022-04-12', '102', '2');
INSERT INTO `db_atm`.`tbl_transactions` (`trans_id`, `description`, `amount`, `date`, `tbl_accounts_acc_ID`, `tbl_accounts_tbl_users_user_id`) VALUES ('6', 'College Fees', '-60000.00', '2022-04-27', '102', '2');
INSERT INTO `db_atm`.`tbl_transactions` (`trans_id`, `description`, `amount`, `date`, `tbl_accounts_acc_ID`, `tbl_accounts_tbl_users_user_id`) VALUES ('7', 'Transfer', '1000.00', '2022-04-02', '103', '3');